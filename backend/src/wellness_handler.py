"""
Wellness log handler for health & wellness voice companion
Monitors agent responses for WELLNESS_COMPLETE_JSON marker and saves to wellness_log.json
"""
import json
import re
from datetime import datetime
from pathlib import Path

WELLNESS_LOG_FILE = Path(__file__).parent.parent / "wellness_log.json"

def load_wellness_history():
    """Load previous wellness check-ins from JSON file"""
    if not WELLNESS_LOG_FILE.exists():
        return []
    
    try:
        with open(WELLNESS_LOG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading wellness history: {e}")
        return []

def get_last_checkin():
    """Get the most recent check-in entry"""
    history = load_wellness_history()
    if history and len(history) > 0:
        return history[-1]
    return None

def extract_wellness_json(text: str):
    """
    Extract wellness check-in JSON from agent response.
    Looks for pattern: WELLNESS_COMPLETE_JSON: {json_object}
    """
    pattern = r'WELLNESS_COMPLETE_JSON:\s*(\{.*?\})'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            # Validate required fields
            required = ["mood", "objectives"]
            if all(field in data for field in required):
                return data
            else:
                print(f"Missing required fields in wellness JSON: {data}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse wellness JSON: {e}")
    
    return None

def save_checkin(checkin_data: dict):
    """
    Append wellness check-in to the log file
    """
    # Add timestamp if not present
    if 'timestamp' not in checkin_data:
        checkin_data['timestamp'] = datetime.now().isoformat()
    
    # Load existing history
    history = load_wellness_history()
    
    # Append new check-in
    history.append(checkin_data)
    
    # Save back to file
    try:
        with open(WELLNESS_LOG_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"✅ Wellness check-in saved: {checkin_data}")
    except Exception as e:
        print(f"❌ Error saving wellness check-in: {e}")

def monitor_wellness_response(response_text: str):
    """
    Monitor agent responses for completed wellness check-ins
    Call this function whenever the agent produces text output
    """
    wellness_data = extract_wellness_json(response_text)
    if wellness_data:
        save_checkin(wellness_data)
        print(f"📊 New wellness check-in recorded at {wellness_data.get('timestamp')}")
