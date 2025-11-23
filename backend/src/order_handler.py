"""Order handling utility for saving completed orders to JSON."""
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger("order_handler")


def extract_order_json(text: str) -> Optional[dict]:
    """Extract order JSON from agent response text.
    
    Looks for the ORDER_COMPLETE_JSON: marker and extracts the JSON object.
    
    Args:
        text: The agent's response text
        
    Returns:
        dict if valid order JSON found, None otherwise
    """
    # Look for the ORDER_COMPLETE_JSON: marker
    match = re.search(r'ORDER_COMPLETE_JSON:\s*(\{.*?\})', text, re.IGNORECASE)
    if not match:
        return None
    
    json_str = match.group(1)
    try:
        order_data = json.loads(json_str)
        # Validate required fields
        required_fields = ['drinkType', 'size', 'milk', 'extras', 'name']
        if all(field in order_data for field in required_fields):
            return order_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse order JSON: {e}")
    
    return None


def save_order(order_data: dict, orders_file: Path = None) -> bool:
    """Save order to orders.json file.
    
    Args:
        order_data: Dictionary containing order information
        orders_file: Path to orders.json file (defaults to backend/orders.json)
        
    Returns:
        True if saved successfully, False otherwise
    """
    if orders_file is None:
        # Default to backend/orders.json
        backend_dir = Path(__file__).parent.parent
        orders_file = backend_dir / "orders.json"
    
    try:
        # Add timestamp to order
        order_with_timestamp = {
            "timestamp": datetime.now().isoformat(),
            **order_data
        }
        
        # Load existing orders or create new list
        if orders_file.exists():
            with open(orders_file, 'r', encoding='utf-8') as f:
                try:
                    orders = json.load(f)
                    if not isinstance(orders, list):
                        orders = []
                except json.JSONDecodeError:
                    orders = []
        else:
            orders = []
        
        # Append new order
        orders.append(order_with_timestamp)
        
        # Save back to file
        with open(orders_file, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Order saved successfully: {order_data.get('name', 'Unknown')}'s {order_data.get('drinkType', 'drink')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to save order: {e}")
        return False


def monitor_agent_response(response_text: str) -> None:
    """Monitor agent responses and automatically save completed orders.
    
    Call this function with every agent response to check for completed orders.
    
    Args:
        response_text: The agent's response text to monitor
    """
    order_data = extract_order_json(response_text)
    if order_data:
        logger.info(f"📝 Detected completed order in response")
        save_order(order_data)
