import logging
import json
import sys
import signal
from pathlib import Path
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram

# Windows signal handling
if sys.platform == 'win32':
    signal.signal(signal.SIGBREAK, signal.SIG_IGN)

logger = logging.getLogger("agent")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.local")

# File paths
CATALOG_PATH = Path(__file__).parent.parent / "catalog.json"
ORDERS_PATH = Path(__file__).parent.parent / "orders.json"
CURRENT_ORDER_PATH = Path(__file__).parent.parent / "current_order.json"

# Load catalog
def load_catalog():
    """Load the product catalog from JSON file"""
    with open(CATALOG_PATH, 'r') as f:
        return json.load(f)

CATALOG = load_catalog()

def get_item_by_id(item_id: str) -> Optional[dict]:
    """Get item details by ID"""
    for category in CATALOG['categories']:
        for item in category['items']:
            if item['id'] == item_id:
                return {**item, 'category': category['name']}
    return None

def search_items(query: str) -> list:
    """Search for items by name (fuzzy match)"""
    query_lower = query.lower()
    results = []
    for category in CATALOG['categories']:
        for item in category['items']:
            if query_lower in item['name'].lower():
                results.append({**item, 'category': category['name']})
    return results

def get_recipe_items(recipe_name: str) -> list:
    """Get items for a recipe/meal"""
    recipe_lower = recipe_name.lower()
    for recipe_key, item_ids in CATALOG.get('recipes', {}).items():
        if recipe_key in recipe_lower or recipe_lower in recipe_key:
            items = []
            for item_id in item_ids:
                item = get_item_by_id(item_id)
                if item:
                    items.append(item)
            return items
    return []


class ShoppingAssistant(Agent):
    """Zepto Express Shopping Assistant Voice Agent"""
    
    def __init__(self):
        super().__init__(
            instructions="""You are Zara, a friendly and efficient shopping assistant for Zepto Express - India's fastest grocery delivery service.

Your job is to help customers order groceries and food items through voice conversation.

PERSONALITY:
- Friendly, upbeat, and helpful
- Quick and efficient (like Zepto's 10-minute delivery!)
- Use casual Indian English naturally
- Be enthusiastic about helping customers

CONVERSATION FLOW:
1. Greet warmly: "Hi there! I'm Zara, your Zepto Express shopping assistant. I can help you order groceries, snacks, fruits, dairy - you name it! What would you like to add to your cart today?"

2. When user requests items:
   - If they ask for specific items (like "add milk"), use add_to_cart tool
   - If they ask for "ingredients for X" or "what I need for X", use get_ingredients_for_recipe tool first, then add those items
   - Always confirm what you've added

3. Cart operations:
   - When asked "what's in my cart", use show_cart tool
   - For "remove X", use remove_from_cart tool
   - For quantity changes, use update_quantity tool

4. Finishing the order:
   - When user says "that's all", "place order", "I'm done", "checkout"
   - Use place_order tool to save the order
   - Confirm the total and thank them

SPEAKING STYLE:
- Keep responses concise but friendly
- Confirm additions: "Added 2 packets of Maggi to your cart! Anything else?"
- For recipes: "For pasta, I'll add pasta and sauce to your cart. Sound good?"
- Read prices when relevant: "Amul Milk is 30 rupees for 500ml"

IMPORTANT:
- Always use tools for cart operations - don't just say you added something
- Confirm cart changes verbally
- If item not found, suggest alternatives
- Keep the conversation flowing naturally

FIRST MESSAGE: "Hi there! I'm Zara from Zepto Express. I can help you order groceries super fast! What would you like to add to your cart today?"
""",
            tts=murf.TTS(voice="en-US-natalie", model="FALCON"),
            llm=google.LLM(model="gemini-2.0-flash"),
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-3"),
        )
        
        # Initialize cart
        self.cart = []
    
    def _calculate_total(self) -> float:
        """Calculate cart total"""
        return sum(item['price'] * item['quantity'] for item in self.cart)
    
    def _format_cart(self) -> str:
        """Format cart for display"""
        if not self.cart:
            return "Your cart is empty."
        
        lines = ["Here's what's in your cart:"]
        for item in self.cart:
            lines.append(f"- {item['name']} x{item['quantity']} = ₹{item['price'] * item['quantity']}")
        lines.append(f"\nTotal: ₹{self._calculate_total()}")
        return "\n".join(lines)
    
    @function_tool()
    async def search_catalog(self, query: str, context: RunContext) -> str:
        """Search for items in the catalog by name"""
        results = search_items(query)
        if not results:
            return f"Sorry, I couldn't find '{query}' in our catalog. Try searching for something else like milk, bread, eggs, or snacks."
        
        lines = [f"Found {len(results)} item(s) matching '{query}':"]
        for item in results[:5]:  # Show max 5 results
            lines.append(f"- {item['name']}: ₹{item['price']}/{item['unit']}")
        return "\n".join(lines)
    
    @function_tool()
    async def add_to_cart(self, item_name: str, quantity: int, context: RunContext) -> str:
        """Add an item to the shopping cart"""
        # Search for the item
        results = search_items(item_name)
        if not results:
            return f"Sorry, I couldn't find '{item_name}' in our catalog. Would you like me to search for something similar?"
        
        item = results[0]  # Take the best match
        
        # Check if item already in cart
        for cart_item in self.cart:
            if cart_item['id'] == item['id']:
                cart_item['quantity'] += quantity
                logger.info(f"🛒 Updated {item['name']} quantity to {cart_item['quantity']}")
                return f"Updated {item['name']} quantity to {cart_item['quantity']}. Your cart total is now ₹{self._calculate_total()}."
        
        # Add new item to cart
        self.cart.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'unit': item['unit'],
            'quantity': quantity
        })
        
        logger.info(f"🛒 Added {quantity}x {item['name']} to cart")
        return f"Added {quantity} {item['name']} (₹{item['price']}/{item['unit']}) to your cart. Cart total: ₹{self._calculate_total()}."
    
    @function_tool()
    async def remove_from_cart(self, item_name: str, context: RunContext) -> str:
        """Remove an item from the shopping cart"""
        item_lower = item_name.lower()
        for i, cart_item in enumerate(self.cart):
            if item_lower in cart_item['name'].lower():
                removed = self.cart.pop(i)
                logger.info(f"🗑️ Removed {removed['name']} from cart")
                return f"Removed {removed['name']} from your cart. Cart total: ₹{self._calculate_total()}."
        
        return f"'{item_name}' is not in your cart."
    
    @function_tool()
    async def update_quantity(self, item_name: str, new_quantity: int, context: RunContext) -> str:
        """Update the quantity of an item in the cart"""
        if new_quantity <= 0:
            return await self.remove_from_cart(item_name, context)
        
        item_lower = item_name.lower()
        for cart_item in self.cart:
            if item_lower in cart_item['name'].lower():
                old_qty = cart_item['quantity']
                cart_item['quantity'] = new_quantity
                logger.info(f"📝 Updated {cart_item['name']} from {old_qty} to {new_quantity}")
                return f"Updated {cart_item['name']} quantity from {old_qty} to {new_quantity}. Cart total: ₹{self._calculate_total()}."
        
        return f"'{item_name}' is not in your cart. Would you like me to add it?"
    
    @function_tool()
    async def show_cart(self, context: RunContext) -> str:
        """Show all items currently in the cart"""
        logger.info(f"🛒 Showing cart with {len(self.cart)} items")
        return self._format_cart()
    
    @function_tool()
    async def get_ingredients_for_recipe(self, recipe_name: str, context: RunContext) -> str:
        """Get and add ingredients for a recipe or meal to the cart"""
        items = get_recipe_items(recipe_name)
        
        if not items:
            return f"I don't have a recipe for '{recipe_name}'. But tell me what you're making and I can help you find the ingredients!"
        
        # Add all items to cart
        added_items = []
        for item in items:
            # Check if already in cart
            found = False
            for cart_item in self.cart:
                if cart_item['id'] == item['id']:
                    cart_item['quantity'] += 1
                    found = True
                    break
            
            if not found:
                self.cart.append({
                    'id': item['id'],
                    'name': item['name'],
                    'price': item['price'],
                    'unit': item['unit'],
                    'quantity': 1
                })
            added_items.append(item['name'])
        
        logger.info(f"🍳 Added recipe items for {recipe_name}: {added_items}")
        return f"For {recipe_name}, I've added: {', '.join(added_items)}. Cart total: ₹{self._calculate_total()}."
    
    @function_tool()
    async def place_order(self, customer_name: str, context: RunContext) -> str:
        """Place the order and save it to JSON file"""
        if not self.cart:
            return "Your cart is empty! Add some items before placing an order."
        
        # Create order object
        order = {
            'order_id': f"ZEP{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'customer_name': customer_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'confirmed',
            'items': self.cart.copy(),
            'total': self._calculate_total(),
            'delivery_estimate': '10 minutes'
        }
        
        # Save current order
        with open(CURRENT_ORDER_PATH, 'w') as f:
            json.dump(order, f, indent=2)
        
        # Append to order history
        orders = []
        if ORDERS_PATH.exists():
            with open(ORDERS_PATH, 'r') as f:
                orders = json.load(f)
        orders.append(order)
        with open(ORDERS_PATH, 'w') as f:
            json.dump(orders, f, indent=2)
        
        logger.info(f"✅ Order {order['order_id']} placed! Total: ₹{order['total']}")
        
        # Clear cart
        cart_summary = self._format_cart()
        self.cart = []
        
        return f"""Order placed successfully!
        
Order ID: {order['order_id']}
{cart_summary}

Your order will arrive in approximately 10 minutes. Thank you for shopping with Zepto Express!"""
    
    @function_tool()
    async def clear_cart(self, context: RunContext) -> str:
        """Clear all items from the cart"""
        self.cart = []
        logger.info("🗑️ Cart cleared")
        return "Cart cleared! What would you like to add?"


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the shopping assistant agent"""
    logger.info("🛒 Starting Zepto Express Shopping Assistant...")
    
    await ctx.connect()
    logger.info("✅ Connected to LiveKit room")
    
    # Create agent instance
    agent = ShoppingAssistant()
    
    # Start the agent session
    session = AgentSession()
    await session.start(agent, room=ctx.room)
    
    logger.info("🎙️ Shopping Assistant is ready to take orders!")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
