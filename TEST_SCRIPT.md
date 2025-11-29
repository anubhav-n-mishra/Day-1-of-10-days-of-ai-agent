# 🎮 Realm of Eldoria - Voice D&D Adventure Test Script

## How to Play
Open **http://localhost:3002** in your browser, click **"BEGIN YOUR QUEST"**, and speak to Dungeon Master Aldric!

---

## 🎭 Test Dialogue Script

### **Opening Scene - The Rusty Tankard Tavern**

*Aldric will set the scene - a stormy night, a distressed woman bursts in asking for help*

---

### **Phase 1: Introduction (Say these)**

1. **"My name is Thorin"** or **"I am called [your name]"**
   - *Aldric will remember your name throughout the adventure*

2. **"I'm a warrior"** or **"I am a rogue"** or **"I'm a mage"**
   - *This affects your attributes (strength, dexterity, or intelligence)*

---

### **Phase 2: Responding to the Quest**

3. **"I'll help you find your brother!"**
   - *Accepts the quest and triggers the story*

4. **"Who is that hooded figure in the corner?"**
   - *Investigate the mysterious NPC*

5. **"I approach the hooded stranger"**
   - *Aldric will describe the encounter and may require a skill check*

---

### **Phase 3: Game Mechanics (Try these!)**

6. **"I roll to persuade the stranger"** or **"I try to intimidate them"**
   - 🎲 *Triggers a D20 dice roll with modifiers*
   - Listen for: "Critical Success!", "Success!", "Failure!", etc.

7. **"What's in my inventory?"** or **"Check my bag"**
   - *Lists your items: sword, armor, torches, etc.*

8. **"What's my health?"** or **"Am I injured?"**
   - *Reports your current HP and status*

---

### **Phase 4: Story Progression**

9. **"I head to Darkwood Forest"** or **"Let's go to the temple"**
   - *Moves the story forward*

10. **"I search the area"** or **"I look for clues"**
    - 🎲 *Triggers a perception/investigation check*

11. **"I attack!"** or **"I draw my sword and fight!"**
    - 🎲 *Combat roll with strength modifier*

---

### **Phase 5: Advanced Commands**

12. **"Give me a summary"** or **"What's happened so far?"**
    - *Full game state: quests, NPCs met, location, gold, etc.*

13. **"I use a torch"** or **"Light my torch"**
    - *Uses an item from inventory*

14. **"I want to buy a health potion"** (if at a shop)
    - *Spends gold on items*

15. **"Restart the adventure"** or **"Start over"**
    - *Resets everything for a fresh game*

---

## 🎲 Cool Things to Try

### **Creative Actions**
- **"I climb the tavern roof to scout the area"** - *Dexterity check!*
- **"I try to charm the barkeep for information"** - *Charisma check!*
- **"I read the ancient runes on the door"** - *Intelligence check!*
- **"I attempt to sneak past the guards"** - *Stealth check!*

### **Combat Scenarios**
- **"I swing my sword at the goblin!"**
- **"I dodge the attack!"**
- **"I cast a fireball!"** (if you're a mage)

### **Roleplay Options**
- **"I buy a round of drinks for the tavern"** - *Spend gold, gain favor*
- **"I threaten the bandits"** - *Intimidation check*
- **"I search the body for loot"** - *Find gold or items*

---

## 🎯 Dice Roll Results Guide

| Roll | Result |
|------|--------|
| 1 | 💀 **CRITICAL FAILURE** - Disaster strikes! |
| 2-9 | ❌ **FAILURE** - Things don't go as planned |
| 10-14 | ⚠️ **PARTIAL SUCCESS** - Success with complications |
| 15-19 | ✅ **SUCCESS** - You accomplish your goal! |
| 20 | 🌟 **CRITICAL SUCCESS** - Legendary outcome! |

---

## 🏆 Story Acts

- **Act 1 (Turns 1-5)**: The Call - Accept the quest, gather information
- **Act 2 (Turns 6-10)**: The Journey - Travel, face challenges, discover secrets
- **Act 3 (Turn 11+)**: The Confrontation - Face the Shadow Dragon Malachar!

---

## 🐛 Troubleshooting

**Voice not working?**
- Click the microphone button to enable it
- Make sure browser has microphone permissions

**Agent not responding?**
- Check that the backend is running: `uv run python src/agent.py dev`
- Check frontend is on port 3002: `pnpm dev`

**"Failed to fetch" error?**
- Restart both backend and frontend
- Make sure .env.local files have correct LiveKit credentials

---

## 🎉 Have Fun, Adventurer!

*"May your rolls be high and your adventures legendary!"*
— Dungeon Master Aldric

