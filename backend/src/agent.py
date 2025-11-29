"""
Day 8: Voice Game Master - D&D Style Adventure
A voice-only game master running epic fantasy adventures in the Realm of Eldoria
Theme: Xbox Game Studios (Green/Black)
"""

import logging
import json
import sys
import signal
import random
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

logger = logging.getLogger("game-master")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.local")

# Game state storage
GAME_STATE_PATH = Path(__file__).parent.parent / "game_state.json"


def save_game_state(state: dict):
    """Save game state to JSON file"""
    with open(GAME_STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)
    logger.info(f"💾 Game state saved")


def load_game_state() -> Optional[dict]:
    """Load game state from JSON file"""
    if GAME_STATE_PATH.exists():
        with open(GAME_STATE_PATH, 'r') as f:
            return json.load(f)
    return None


def roll_dice(sides: int = 20, modifier: int = 0) -> tuple[int, int, str]:
    """Roll a dice and return (roll, total, result_tier)"""
    roll = random.randint(1, sides)
    total = roll + modifier
    
    if roll == 1:
        tier = "CRITICAL FAILURE"
    elif roll == 20:
        tier = "CRITICAL SUCCESS"
    elif total >= 15:
        tier = "SUCCESS"
    elif total >= 10:
        tier = "PARTIAL SUCCESS"
    else:
        tier = "FAILURE"
    
    return roll, total, tier


class GameMasterAgent(Agent):
    """D&D-Style Voice Game Master Agent - Dungeon Master Aldric"""
    
    def __init__(self):
        super().__init__(
            instructions="""You are DUNGEON MASTER ALDRIC, a legendary storyteller running an epic fantasy adventure in the Realm of Eldoria.

UNIVERSE: The Realm of Eldoria
- A high-fantasy world of dragons, ancient magic, mysterious ruins, and legendary heroes
- The kingdom is threatened by the awakening of the Shadow Dragon Malachar in the Darkwood Temple
- Magic flows through the land in many forms: elemental, divine, arcane, and forbidden shadow magic
- The world has diverse regions: peaceful villages, dark forests, ancient ruins, mountain fortresses

YOUR PERSONALITY AS ALDRIC:
- Dramatic and theatrical - paint vivid pictures with your words
- Fair but challenging - heroes must earn their victories
- Use rich sensory details (sights, sounds, smells, textures)
- Add humor through quirky NPCs and unexpected situations
- Build tension and suspense masterfully
- Speak with gravitas befitting a master storyteller

STORYTELLING RULES:
1. ALWAYS describe the scene vividly BEFORE asking what the player does
2. END EVERY response with a clear prompt: "What do you do, adventurer?" or a specific choice
3. REMEMBER all past decisions - reference them naturally in the story
4. NPCs have distinct personalities and remember past interactions
5. Consequences MATTER - choices affect the story permanently
6. Combat is dramatic and descriptive, not mechanical
7. Keep responses 2-4 paragraphs - atmospheric but concise
8. Use the function tools to track game state, inventory, health, etc.

STORY STRUCTURE:
- Act 1 (Turns 1-5): The Call - Player starts in Millbrook tavern, hears of trouble
- Act 2 (Turns 6-10): The Journey - Investigation, travel, discovery
- Act 3 (Turns 11+): The Confrontation - Face the darkness

GAME MECHANICS:
- When player attempts risky actions, use roll_skill_check tool
- Track inventory with add_item and remove_item tools
- Update health when player takes damage or heals
- Record important NPCs met and quests accepted

PLAYER INTERACTION:
- If player seems stuck, offer subtle hints through NPCs or environment
- Reward creative solutions - clever thinking beats brute force
- If player tries impossible things, narrate a dramatic failure but give another chance
- Answer questions about inventory, health, or the world when asked

FIRST MESSAGE (say this when starting):
"Welcome, brave adventurer, to the Realm of Eldoria! I am Aldric, your Dungeon Master, and together we shall weave a tale of courage and peril!

The rain hammers against the windows of the Rusty Tankard tavern in the village of Millbrook. You sit by the crackling hearth, nursing a mug of warm spiced ale. The tavern is nearly empty tonight - just old Bertram the barkeep polishing glasses, and a mysterious hooded figure in the far corner who hasn't moved in an hour.

Suddenly, the door bursts open with a crash! A young woman stumbles in, her clothes torn and muddy, desperation in her eyes. 'Please!' she gasps, clutching the doorframe. 'My brother went to investigate the old temple in Darkwood Forest three days ago... he hasn't returned! The village guard won't help - they're too afraid!'

The hooded figure in the corner shifts slightly. Bertram drops his glass with a clatter.

What do you do, adventurer?"
""",
            tts=murf.TTS(voice="en-US-ken", model="FALCON"),
            llm=google.LLM(model="gemini-2.0-flash"),
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-3"),
        )
        
        # Initialize game state
        self.game_state = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "player": {
                "name": "Unknown Hero",
                "class": "Adventurer",
                "health": 100,
                "max_health": 100,
                "status": "Healthy",
                "gold": 25,
                "attributes": {
                    "strength": 12,
                    "dexterity": 10,
                    "intelligence": 10,
                    "charisma": 11,
                    "luck": 10
                },
                "inventory": [
                    {"name": "Worn Leather Armor", "type": "armor", "description": "Basic protection"},
                    {"name": "Iron Sword", "type": "weapon", "description": "A reliable blade"},
                    {"name": "Waterskin", "type": "consumable", "description": "Fresh water"},
                    {"name": "Torch", "type": "tool", "description": "Lights the darkness", "quantity": 3}
                ]
            },
            "current_location": "Rusty Tankard Tavern, Millbrook Village",
            "npcs": [],
            "quests": [],
            "events": [],
            "turn_count": 0,
            "story_act": "Act 1 - The Call to Adventure"
        }
        
        logger.info(f"🎮 New adventure started: {self.game_state['session_id']}")
    
    def _get_attribute_modifier(self, attribute: str) -> int:
        """Get modifier for an attribute"""
        value = self.game_state["player"]["attributes"].get(attribute, 10)
        return (value - 10) // 2
    
    @function_tool()
    async def set_player_info(self, name: str = None, player_class: str = None, context: RunContext = None) -> str:
        """Set the player's name and/or class when they introduce themselves"""
        if name:
            self.game_state["player"]["name"] = name
            logger.info(f"📝 Player name: {name}")
        if player_class:
            self.game_state["player"]["class"] = player_class
            # Adjust attributes based on class
            if player_class.lower() in ["warrior", "fighter", "knight"]:
                self.game_state["player"]["attributes"]["strength"] = 15
                self.game_state["player"]["attributes"]["dexterity"] = 12
            elif player_class.lower() in ["rogue", "thief", "ranger"]:
                self.game_state["player"]["attributes"]["dexterity"] = 15
                self.game_state["player"]["attributes"]["luck"] = 13
            elif player_class.lower() in ["mage", "wizard", "sorcerer"]:
                self.game_state["player"]["attributes"]["intelligence"] = 15
                self.game_state["player"]["attributes"]["charisma"] = 12
            logger.info(f"⚔️ Player class: {player_class}")
        
        save_game_state(self.game_state)
        return f"Player info updated: {self.game_state['player']['name']} the {self.game_state['player']['class']}"
    
    @function_tool()
    async def roll_skill_check(self, skill: str, difficulty: int = 12, context: RunContext = None) -> str:
        """Roll a d20 skill check with appropriate modifier. Use for risky or uncertain actions."""
        # Map skill to attribute
        skill_map = {
            "strength": "strength", "athletics": "strength", "climb": "strength", "break": "strength",
            "dexterity": "dexterity", "stealth": "dexterity", "acrobatics": "dexterity", "dodge": "dexterity",
            "intelligence": "intelligence", "knowledge": "intelligence", "investigate": "intelligence", "arcana": "intelligence",
            "charisma": "charisma", "persuasion": "charisma", "intimidation": "charisma", "deception": "charisma",
            "luck": "luck", "perception": "luck", "survival": "luck"
        }
        
        attribute = skill_map.get(skill.lower(), "luck")
        modifier = self._get_attribute_modifier(attribute)
        
        roll, total, tier = roll_dice(20, modifier)
        success = total >= difficulty
        
        result = f"🎲 DICE ROLL: {roll} + {modifier} ({attribute}) = {total} vs DC {difficulty}\n"
        result += f"Result: {tier}!"
        
        logger.info(f"🎲 {skill} check: {roll}+{modifier}={total} vs DC{difficulty} -> {tier}")
        return result
    
    @function_tool()
    async def add_item(self, item_name: str, item_type: str = "misc", description: str = "", quantity: int = 1, context: RunContext = None) -> str:
        """Add an item to the player's inventory"""
        # Check if item already exists
        for item in self.game_state["player"]["inventory"]:
            if item["name"].lower() == item_name.lower():
                if "quantity" in item:
                    item["quantity"] += quantity
                else:
                    item["quantity"] = quantity + 1
                save_game_state(self.game_state)
                logger.info(f"🎒 Updated {item_name} quantity")
                return f"Added {quantity} more {item_name} to inventory"
        
        new_item = {
            "name": item_name,
            "type": item_type,
            "description": description
        }
        if quantity > 1:
            new_item["quantity"] = quantity
            
        self.game_state["player"]["inventory"].append(new_item)
        save_game_state(self.game_state)
        logger.info(f"🎒 Added {item_name} to inventory")
        return f"Added {item_name} to inventory: {description}"
    
    @function_tool()
    async def remove_item(self, item_name: str, quantity: int = 1, context: RunContext = None) -> str:
        """Remove an item from the player's inventory"""
        for i, item in enumerate(self.game_state["player"]["inventory"]):
            if item_name.lower() in item["name"].lower():
                if "quantity" in item and item["quantity"] > quantity:
                    item["quantity"] -= quantity
                    save_game_state(self.game_state)
                    return f"Used {quantity} {item_name}. {item['quantity']} remaining."
                else:
                    removed = self.game_state["player"]["inventory"].pop(i)
                    save_game_state(self.game_state)
                    logger.info(f"🎒 Removed {removed['name']} from inventory")
                    return f"Removed {removed['name']} from inventory"
        
        return f"{item_name} not found in inventory"
    
    @function_tool()
    async def check_inventory(self, context: RunContext = None) -> str:
        """Check the player's current inventory"""
        inventory = self.game_state["player"]["inventory"]
        if not inventory:
            return "Your pack is empty."
        
        lines = ["Current inventory:"]
        for item in inventory:
            qty = f" x{item['quantity']}" if "quantity" in item else ""
            lines.append(f"- {item['name']}{qty} ({item['type']})")
        lines.append(f"\nGold: {self.game_state['player']['gold']} coins")
        
        logger.info(f"🎒 Inventory checked: {len(inventory)} items")
        return "\n".join(lines)
    
    @function_tool()
    async def update_health(self, change: int, reason: str = "", context: RunContext = None) -> str:
        """Update player health. Positive = healing, negative = damage."""
        player = self.game_state["player"]
        old_health = player["health"]
        player["health"] = max(0, min(player["max_health"], old_health + change))
        new_health = player["health"]
        
        # Update status
        if new_health <= 0:
            player["status"] = "Unconscious"
        elif new_health <= 25:
            player["status"] = "Critical"
        elif new_health <= 50:
            player["status"] = "Injured"
        elif new_health <= 75:
            player["status"] = "Wounded"
        else:
            player["status"] = "Healthy"
        
        save_game_state(self.game_state)
        
        if change > 0:
            logger.info(f"❤️ Healed {change} HP: {old_health} -> {new_health}")
            return f"Healed {change} HP! Health: {new_health}/{player['max_health']} ({player['status']})"
        else:
            logger.info(f"💔 Took {abs(change)} damage: {old_health} -> {new_health}")
            return f"Took {abs(change)} damage from {reason}! Health: {new_health}/{player['max_health']} ({player['status']})"
    
    @function_tool()
    async def check_health(self, context: RunContext = None) -> str:
        """Check player's current health status"""
        player = self.game_state["player"]
        return f"Health: {player['health']}/{player['max_health']} - Status: {player['status']}"
    
    @function_tool()
    async def change_location(self, new_location: str, context: RunContext = None) -> str:
        """Update the player's current location"""
        old_loc = self.game_state["current_location"]
        self.game_state["current_location"] = new_location
        save_game_state(self.game_state)
        logger.info(f"📍 Location: {old_loc} -> {new_location}")
        return f"Traveled from {old_loc} to {new_location}"
    
    @function_tool()
    async def meet_npc(self, name: str, role: str, attitude: str = "neutral", description: str = "", context: RunContext = None) -> str:
        """Record meeting a new NPC"""
        # Check if NPC already exists
        for npc in self.game_state["npcs"]:
            if npc["name"].lower() == name.lower():
                npc["attitude"] = attitude
                npc["last_seen"] = self.game_state["current_location"]
                save_game_state(self.game_state)
                return f"Updated {name}'s attitude to {attitude}"
        
        npc = {
            "name": name,
            "role": role,
            "attitude": attitude,
            "description": description,
            "met_at": self.game_state["current_location"],
            "last_seen": self.game_state["current_location"]
        }
        self.game_state["npcs"].append(npc)
        save_game_state(self.game_state)
        logger.info(f"👤 Met NPC: {name} ({role}, {attitude})")
        return f"Met {name} the {role} ({attitude})"
    
    @function_tool()
    async def add_quest(self, quest_name: str, description: str, giver: str = "", status: str = "active", context: RunContext = None) -> str:
        """Add or update a quest"""
        # Check if quest exists
        for quest in self.game_state["quests"]:
            if quest["name"].lower() == quest_name.lower():
                quest["status"] = status
                save_game_state(self.game_state)
                logger.info(f"📜 Quest updated: {quest_name} -> {status}")
                return f"Quest '{quest_name}' is now {status}"
        
        quest = {
            "name": quest_name,
            "description": description,
            "giver": giver,
            "status": status,
            "started_at": self.game_state["current_location"],
            "turn_started": self.game_state["turn_count"]
        }
        self.game_state["quests"].append(quest)
        save_game_state(self.game_state)
        logger.info(f"📜 New quest: {quest_name}")
        return f"Quest accepted: {quest_name}"
    
    @function_tool()
    async def record_event(self, event: str, importance: str = "normal", context: RunContext = None) -> str:
        """Record an important story event"""
        event_record = {
            "event": event,
            "location": self.game_state["current_location"],
            "turn": self.game_state["turn_count"],
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        }
        self.game_state["events"].append(event_record)
        save_game_state(self.game_state)
        logger.info(f"⚡ Event: {event}")
        return f"Recorded: {event}"
    
    @function_tool()
    async def advance_turn(self, context: RunContext = None) -> str:
        """Advance the turn counter and update story act"""
        self.game_state["turn_count"] += 1
        turn = self.game_state["turn_count"]
        
        # Update story act
        if turn >= 11:
            self.game_state["story_act"] = "Act 3 - The Confrontation"
        elif turn >= 6:
            self.game_state["story_act"] = "Act 2 - The Journey"
        else:
            self.game_state["story_act"] = "Act 1 - The Call"
        
        save_game_state(self.game_state)
        logger.info(f"⏩ Turn {turn}: {self.game_state['story_act']}")
        return f"Turn {turn}. {self.game_state['story_act']}"
    
    @function_tool()
    async def get_game_summary(self, context: RunContext = None) -> str:
        """Get a summary of the current game state"""
        state = self.game_state
        player = state["player"]
        
        # Active quests
        active_quests = [q["name"] for q in state["quests"] if q["status"] == "active"]
        
        # Recent NPCs
        recent_npcs = [f"{n['name']} ({n['attitude']})" for n in state["npcs"][-3:]]
        
        summary = f"""
=== GAME STATE ===
Player: {player['name']} the {player['class']}
Health: {player['health']}/{player['max_health']} ({player['status']})
Gold: {player['gold']}
Location: {state['current_location']}
Story: {state['story_act']} (Turn {state['turn_count']})
Active Quests: {', '.join(active_quests) if active_quests else 'None'}
Recent NPCs: {', '.join(recent_npcs) if recent_npcs else 'None yet'}
==================
"""
        logger.info(f"📊 Game summary requested")
        return summary
    
    @function_tool()
    async def update_gold(self, change: int, reason: str = "", context: RunContext = None) -> str:
        """Update player's gold. Positive = gain, negative = spend."""
        old_gold = self.game_state["player"]["gold"]
        self.game_state["player"]["gold"] = max(0, old_gold + change)
        new_gold = self.game_state["player"]["gold"]
        save_game_state(self.game_state)
        
        if change > 0:
            logger.info(f"💰 Gained {change} gold: {old_gold} -> {new_gold}")
            return f"Gained {change} gold! Total: {new_gold}"
        else:
            logger.info(f"💸 Spent {abs(change)} gold: {old_gold} -> {new_gold}")
            return f"Spent {abs(change)} gold{' on ' + reason if reason else ''}. Remaining: {new_gold}"
    
    @function_tool()
    async def restart_adventure(self, context: RunContext = None) -> str:
        """Restart the game with a fresh state"""
        self.game_state = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "player": {
                "name": "Unknown Hero",
                "class": "Adventurer",
                "health": 100,
                "max_health": 100,
                "status": "Healthy",
                "gold": 25,
                "attributes": {
                    "strength": 12,
                    "dexterity": 10,
                    "intelligence": 10,
                    "charisma": 11,
                    "luck": 10
                },
                "inventory": [
                    {"name": "Worn Leather Armor", "type": "armor", "description": "Basic protection"},
                    {"name": "Iron Sword", "type": "weapon", "description": "A reliable blade"},
                    {"name": "Waterskin", "type": "consumable", "description": "Fresh water"},
                    {"name": "Torch", "type": "tool", "description": "Lights the darkness", "quantity": 3}
                ]
            },
            "current_location": "Rusty Tankard Tavern, Millbrook Village",
            "npcs": [],
            "quests": [],
            "events": [],
            "turn_count": 0,
            "story_act": "Act 1 - The Call to Adventure"
        }
        save_game_state(self.game_state)
        logger.info(f"🔄 Adventure restarted! New session: {self.game_state['session_id']}")
        return "A new adventure begins! The slate is clean, hero."


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the Game Master agent"""
    logger.info("🎲 Starting Dungeon Master Aldric...")
    
    await ctx.connect()
    logger.info("✅ Connected to LiveKit room")
    
    agent = GameMasterAgent()
    session = AgentSession()
    await session.start(agent, room=ctx.room)
    
    logger.info("🏰 The Dungeon Master awaits your adventure!")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
