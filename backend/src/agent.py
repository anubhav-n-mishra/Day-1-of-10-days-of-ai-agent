"""
Day 9: E-commerce Agent - ACP-Inspired Voice Shopping Assistant
A voice-driven shopping assistant following the Agentic Commerce Protocol pattern
Theme: Amazon-inspired (Orange/Dark)
"""

import logging
import json
import sys
import signal
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

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

logger = logging.getLogger("ecommerce-agent")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.local")

# File paths for persistence
ORDERS_PATH = Path(__file__).parent.parent / "acp_orders.json"
CATALOG_PATH = Path(__file__).parent.parent / "acp_catalog.json"

# ============================================================================
# ACP-INSPIRED PRODUCT CATALOG
# ============================================================================

PRODUCTS = [
    # Electronics
    {
        "id": "elec-001",
        "name": "Wireless Bluetooth Earbuds Pro",
        "description": "Premium noise-cancelling earbuds with 30-hour battery life",
        "price": 2999,
        "currency": "INR",
        "category": "electronics",
        "brand": "SoundMax",
        "color": "black",
        "in_stock": True,
        "rating": 4.5
    },
    {
        "id": "elec-002",
        "name": "Smart Watch Series X",
        "description": "Fitness tracker with heart rate monitor and GPS",
        "price": 4999,
        "currency": "INR",
        "category": "electronics",
        "brand": "TechFit",
        "color": "silver",
        "in_stock": True,
        "rating": 4.3
    },
    {
        "id": "elec-003",
        "name": "Portable Power Bank 20000mAh",
        "description": "Fast charging power bank with dual USB ports",
        "price": 1499,
        "currency": "INR",
        "category": "electronics",
        "brand": "PowerUp",
        "color": "white",
        "in_stock": True,
        "rating": 4.6
    },
    # Clothing
    {
        "id": "cloth-001",
        "name": "Premium Cotton T-Shirt",
        "description": "Soft breathable cotton t-shirt, perfect for daily wear",
        "price": 599,
        "currency": "INR",
        "category": "clothing",
        "brand": "ComfortWear",
        "color": "navy blue",
        "sizes": ["S", "M", "L", "XL"],
        "in_stock": True,
        "rating": 4.2
    },
    {
        "id": "cloth-002",
        "name": "Classic Denim Jeans",
        "description": "Slim fit denim jeans with stretch comfort",
        "price": 1299,
        "currency": "INR",
        "category": "clothing",
        "brand": "DenimCo",
        "color": "dark blue",
        "sizes": ["28", "30", "32", "34", "36"],
        "in_stock": True,
        "rating": 4.4
    },
    {
        "id": "cloth-003",
        "name": "Winter Hoodie Jacket",
        "description": "Warm fleece-lined hoodie with front pocket",
        "price": 1599,
        "currency": "INR",
        "category": "clothing",
        "brand": "WarmStyle",
        "color": "black",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "in_stock": True,
        "rating": 4.7
    },
    {
        "id": "cloth-004",
        "name": "Sports Running Shoes",
        "description": "Lightweight mesh running shoes with cushioned sole",
        "price": 2499,
        "currency": "INR",
        "category": "footwear",
        "brand": "SpeedRun",
        "color": "red",
        "sizes": ["7", "8", "9", "10", "11"],
        "in_stock": True,
        "rating": 4.5
    },
    # Home & Kitchen
    {
        "id": "home-001",
        "name": "Stainless Steel Coffee Mug",
        "description": "Double-wall insulated mug keeps drinks hot for hours",
        "price": 449,
        "currency": "INR",
        "category": "kitchen",
        "brand": "HomeEssentials",
        "color": "silver",
        "capacity": "350ml",
        "in_stock": True,
        "rating": 4.3
    },
    {
        "id": "home-002",
        "name": "Ceramic Coffee Mug Set",
        "description": "Set of 4 beautiful ceramic mugs with floral design",
        "price": 799,
        "currency": "INR",
        "category": "kitchen",
        "brand": "ArtisanCraft",
        "color": "white",
        "capacity": "300ml each",
        "in_stock": True,
        "rating": 4.6
    },
    {
        "id": "home-003",
        "name": "Non-Stick Frying Pan",
        "description": "Premium non-stick pan with heat-resistant handle",
        "price": 899,
        "currency": "INR",
        "category": "kitchen",
        "brand": "ChefPro",
        "color": "black",
        "size": "26cm",
        "in_stock": True,
        "rating": 4.4
    },
    # Books
    {
        "id": "book-001",
        "name": "The Art of Programming",
        "description": "Comprehensive guide to modern software development",
        "price": 699,
        "currency": "INR",
        "category": "books",
        "author": "John Smith",
        "format": "paperback",
        "in_stock": True,
        "rating": 4.8
    },
    {
        "id": "book-002",
        "name": "AI Revolution: Future of Technology",
        "description": "Exploring the impact of artificial intelligence on society",
        "price": 549,
        "currency": "INR",
        "category": "books",
        "author": "Sarah Johnson",
        "format": "paperback",
        "in_stock": True,
        "rating": 4.5
    },
    # Personal Care
    {
        "id": "care-001",
        "name": "Organic Face Moisturizer",
        "description": "Natural moisturizer with aloe vera and vitamin E",
        "price": 399,
        "currency": "INR",
        "category": "personal care",
        "brand": "NaturGlow",
        "size": "100ml",
        "in_stock": True,
        "rating": 4.4
    },
    {
        "id": "care-002",
        "name": "Electric Beard Trimmer",
        "description": "Precision trimmer with multiple length settings",
        "price": 1299,
        "currency": "INR",
        "category": "personal care",
        "brand": "GroomMaster",
        "color": "black",
        "in_stock": True,
        "rating": 4.3
    },
]


# ============================================================================
# ACP-INSPIRED COMMERCE LAYER
# ============================================================================

def load_orders() -> List[Dict]:
    """Load orders from JSON file"""
    if ORDERS_PATH.exists():
        with open(ORDERS_PATH, 'r') as f:
            return json.load(f)
    return []


def save_orders(orders: List[Dict]):
    """Save orders to JSON file"""
    with open(ORDERS_PATH, 'w') as f:
        json.dump(orders, f, indent=2, default=str)


def list_products(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    min_price: Optional[int] = None,
    color: Optional[str] = None,
    search_query: Optional[str] = None,
    brand: Optional[str] = None
) -> List[Dict]:
    """
    ACP-inspired catalog query function.
    Filters products based on various criteria.
    """
    results = PRODUCTS.copy()
    
    if category:
        category_lower = category.lower()
        results = [p for p in results if category_lower in p.get("category", "").lower()]
    
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    
    if min_price:
        results = [p for p in results if p["price"] >= min_price]
    
    if color:
        color_lower = color.lower()
        results = [p for p in results if color_lower in p.get("color", "").lower()]
    
    if brand:
        brand_lower = brand.lower()
        results = [p for p in results if brand_lower in p.get("brand", "").lower()]
    
    if search_query:
        query_lower = search_query.lower()
        results = [p for p in results if 
                   query_lower in p["name"].lower() or 
                   query_lower in p.get("description", "").lower() or
                   query_lower in p.get("category", "").lower()]
    
    return results


def get_product_by_id(product_id: str) -> Optional[Dict]:
    """Get a specific product by ID"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def create_order(line_items: List[Dict], buyer_name: str = "Guest") -> Dict:
    """
    ACP-inspired order creation function.
    Creates an order with proper structure following ACP patterns.
    
    line_items: [{"product_id": "...", "quantity": 1, "size": "M"}, ...]
    """
    orders = load_orders()
    
    # Generate order ID
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    # Build order items with full product details
    order_items = []
    total = 0
    
    for item in line_items:
        product = get_product_by_id(item["product_id"])
        if product:
            quantity = item.get("quantity", 1)
            item_total = product["price"] * quantity
            total += item_total
            
            order_item = {
                "product_id": product["id"],
                "product_name": product["name"],
                "unit_price": product["price"],
                "quantity": quantity,
                "line_total": item_total,
                "currency": product["currency"]
            }
            
            # Add size if specified
            if "size" in item:
                order_item["size"] = item["size"]
            
            # Add color
            if "color" in product:
                order_item["color"] = product["color"]
                
            order_items.append(order_item)
    
    # Create the order object (ACP-inspired structure)
    order = {
        "id": order_id,
        "status": "CONFIRMED",
        "buyer": {
            "name": buyer_name
        },
        "line_items": order_items,
        "totals": {
            "subtotal": total,
            "tax": round(total * 0.18),  # 18% GST
            "total": round(total * 1.18),
            "currency": "INR"
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    orders.append(order)
    save_orders(orders)
    
    logger.info(f"📦 Order created: {order_id} - Total: ₹{order['totals']['total']}")
    return order


def get_order_by_id(order_id: str) -> Optional[Dict]:
    """Get a specific order by ID"""
    orders = load_orders()
    for order in orders:
        if order["id"] == order_id:
            return order
    return None


def get_recent_orders(limit: int = 5) -> List[Dict]:
    """Get the most recent orders"""
    orders = load_orders()
    return orders[-limit:] if orders else []


def get_last_order() -> Optional[Dict]:
    """Get the most recent order"""
    orders = load_orders()
    return orders[-1] if orders else None


# ============================================================================
# ECOMMERCE VOICE AGENT
# ============================================================================

class EcommerceAgent(Agent):
    """ACP-Inspired Voice Shopping Assistant"""
    
    def __init__(self):
        super().__init__(
            instructions="""You are ARIA, a friendly and helpful voice shopping assistant for an online store.

YOUR PERSONALITY:
- Warm, helpful, and professional
- Enthusiastic about helping customers find the perfect products
- Clear and concise in descriptions
- Always confirm details before placing orders
- Use natural conversational language

YOUR CAPABILITIES:
1. BROWSE CATALOG: Help users explore products by category, price, color, or search terms
2. PRODUCT DETAILS: Provide detailed information about specific products
3. PLACE ORDERS: Create orders when users want to buy
4. ORDER STATUS: Tell users about their recent orders

CONVERSATION GUIDELINES:

When showing products:
- Mention 2-4 products at a time, not all at once
- Include name, price, and one key feature
- Ask if they want more details or to see more options

When user wants to buy:
- Confirm the exact product they want
- Ask for size if it's clothing/footwear
- Summarize the order before confirming
- Provide the order ID after creation

Price format:
- Always say prices in Rupees (e.g., "Rupees 599" or "₹599")
- Mention if there are any deals or ratings

AVAILABLE CATEGORIES:
- Electronics (earbuds, smartwatch, power bank)
- Clothing (t-shirts, jeans, hoodies)
- Footwear (running shoes)
- Kitchen (mugs, pans)
- Books (programming, AI)
- Personal Care (moisturizer, trimmer)

FIRST MESSAGE:
"Hello! I'm Aria, your shopping assistant. I'm here to help you find exactly what you're looking for! 

We have great products in electronics, clothing, kitchen essentials, books, and more. 

What can I help you find today? You can say things like 'Show me t-shirts' or 'I'm looking for earbuds under 3000 rupees'."
""",
            tts=murf.TTS(voice="en-US-natalie", model="FALCON"),
            llm=google.LLM(model="gemini-2.0-flash"),
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-3"),
        )
        
        # Session context for tracking conversation
        self.session_context = {
            "last_shown_products": [],
            "cart": [],
            "buyer_name": "Guest"
        }
        
        logger.info("🛒 Aria E-commerce Agent initialized")
    
    @function_tool()
    async def search_products(
        self, 
        query: str = None,
        category: str = None, 
        max_price: int = None,
        min_price: int = None,
        color: str = None,
        brand: str = None,
        context: RunContext = None
    ) -> str:
        """
        Search the product catalog with various filters.
        Use this when user wants to browse or find products.
        """
        products = list_products(
            category=category,
            max_price=max_price,
            min_price=min_price,
            color=color,
            search_query=query,
            brand=brand
        )
        
        if not products:
            return "No products found matching your criteria. Try different filters or browse our categories: electronics, clothing, kitchen, books, personal care."
        
        # Store for reference
        self.session_context["last_shown_products"] = products
        
        # Format results
        result_lines = [f"Found {len(products)} product(s):\n"]
        for i, p in enumerate(products[:5], 1):  # Show max 5
            rating = f"⭐ {p.get('rating', 'N/A')}" if p.get('rating') else ""
            colors = f", {p.get('color', '')}" if p.get('color') else ""
            result_lines.append(
                f"{i}. {p['name']} - ₹{p['price']} {rating}{colors}"
            )
        
        if len(products) > 5:
            result_lines.append(f"\n...and {len(products) - 5} more. Ask to see more!")
        
        logger.info(f"🔍 Search returned {len(products)} products")
        return "\n".join(result_lines)
    
    @function_tool()
    async def get_product_details(self, product_number: int = None, product_id: str = None, context: RunContext = None) -> str:
        """
        Get detailed information about a specific product.
        Use product_number (1-5) from the last search, or product_id directly.
        """
        product = None
        
        if product_number and self.session_context["last_shown_products"]:
            idx = product_number - 1
            if 0 <= idx < len(self.session_context["last_shown_products"]):
                product = self.session_context["last_shown_products"][idx]
        elif product_id:
            product = get_product_by_id(product_id)
        
        if not product:
            return "Product not found. Please search for products first or provide a valid product number."
        
        # Build detailed description
        details = [
            f"📦 {product['name']}",
            f"💰 Price: ₹{product['price']}",
            f"📝 {product.get('description', 'No description')}",
            f"🏷️ Brand: {product.get('brand', 'N/A')}",
            f"🎨 Color: {product.get('color', 'N/A')}",
            f"⭐ Rating: {product.get('rating', 'N/A')}/5",
        ]
        
        if product.get('sizes'):
            details.append(f"📏 Sizes available: {', '.join(product['sizes'])}")
        
        if product.get('in_stock'):
            details.append("✅ In Stock - Ready to ship!")
        else:
            details.append("❌ Currently out of stock")
        
        details.append(f"\nProduct ID: {product['id']}")
        
        logger.info(f"📋 Showing details for: {product['name']}")
        return "\n".join(details)
    
    @function_tool()
    async def set_buyer_name(self, name: str, context: RunContext = None) -> str:
        """Set the buyer's name for the order"""
        self.session_context["buyer_name"] = name
        logger.info(f"👤 Buyer name set: {name}")
        return f"Great! I'll add the order under the name: {name}"
    
    @function_tool()
    async def place_order(
        self, 
        product_number: int = None,
        product_id: str = None,
        quantity: int = 1,
        size: str = None,
        context: RunContext = None
    ) -> str:
        """
        Place an order for a product.
        Use product_number (1-5) from last search, or product_id directly.
        Include size for clothing/footwear.
        """
        product = None
        
        if product_number and self.session_context["last_shown_products"]:
            idx = product_number - 1
            if 0 <= idx < len(self.session_context["last_shown_products"]):
                product = self.session_context["last_shown_products"][idx]
        elif product_id:
            product = get_product_by_id(product_id)
        
        if not product:
            return "Product not found. Please search for products first and tell me which one you'd like to order."
        
        # Check if size is needed
        if product.get('sizes') and not size:
            return f"This product comes in sizes: {', '.join(product['sizes'])}. Please specify your size."
        
        # Create line item
        line_item = {
            "product_id": product["id"],
            "quantity": quantity
        }
        if size:
            line_item["size"] = size
        
        # Create the order
        order = create_order(
            line_items=[line_item],
            buyer_name=self.session_context["buyer_name"]
        )
        
        # Format confirmation
        confirmation = [
            "🎉 Order Confirmed!",
            f"📋 Order ID: {order['id']}",
            f"👤 Buyer: {order['buyer']['name']}",
            "",
            "Items ordered:"
        ]
        
        for item in order["line_items"]:
            size_info = f" (Size: {item['size']})" if item.get('size') else ""
            confirmation.append(f"  • {item['product_name']}{size_info} x{item['quantity']} - ₹{item['line_total']}")
        
        confirmation.extend([
            "",
            f"💰 Subtotal: ₹{order['totals']['subtotal']}",
            f"📊 Tax (18% GST): ₹{order['totals']['tax']}",
            f"💳 Total: ₹{order['totals']['total']}",
            "",
            "Thank you for shopping with us! Your order will be delivered soon."
        ])
        
        logger.info(f"✅ Order placed: {order['id']}")
        return "\n".join(confirmation)
    
    @function_tool()
    async def get_last_order(self, context: RunContext = None) -> str:
        """Get details of the most recent order"""
        order = get_last_order()
        
        if not order:
            return "You haven't placed any orders yet. Would you like to browse our products?"
        
        summary = [
            f"📦 Your Last Order:",
            f"Order ID: {order['id']}",
            f"Status: {order['status']}",
            f"Placed: {order['created_at'][:10]}",
            "",
            "Items:"
        ]
        
        for item in order["line_items"]:
            size_info = f" (Size: {item.get('size', '')})" if item.get('size') else ""
            summary.append(f"  • {item['product_name']}{size_info} x{item['quantity']}")
        
        summary.append(f"\nTotal: ₹{order['totals']['total']}")
        
        logger.info(f"📋 Retrieved last order: {order['id']}")
        return "\n".join(summary)
    
    @function_tool()
    async def get_order_history(self, limit: int = 3, context: RunContext = None) -> str:
        """Get recent order history"""
        orders = get_recent_orders(limit)
        
        if not orders:
            return "No order history found. Start shopping to create your first order!"
        
        summary = [f"📜 Your Last {len(orders)} Order(s):\n"]
        
        for order in reversed(orders):
            item_names = [item["product_name"] for item in order["line_items"]]
            summary.append(
                f"• {order['id']} - ₹{order['totals']['total']} - {', '.join(item_names[:2])}"
            )
        
        logger.info(f"📜 Retrieved {len(orders)} orders")
        return "\n".join(summary)
    
    @function_tool()
    async def get_categories(self, context: RunContext = None) -> str:
        """List all available product categories"""
        categories = set(p.get("category", "other") for p in PRODUCTS)
        
        category_counts = {}
        for p in PRODUCTS:
            cat = p.get("category", "other")
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        result = ["🏪 Available Categories:\n"]
        for cat, count in sorted(category_counts.items()):
            result.append(f"  • {cat.title()} ({count} products)")
        
        result.append("\nJust say a category name to browse products!")
        
        return "\n".join(result)


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the E-commerce agent"""
    logger.info("🛒 Starting Aria E-commerce Agent...")
    
    await ctx.connect()
    logger.info("✅ Connected to LiveKit room")
    
    agent = EcommerceAgent()
    session = AgentSession()
    await session.start(agent, room=ctx.room)
    
    logger.info("🛍️ Aria is ready to help customers shop!")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
