# Day 3: Health & Wellness Voice Companion

## Overview
A supportive daily wellness check-in companion that uses voice AI to help users reflect on their mood, set intentions, and track their wellbeing over time.

## ✅ Primary Goal Implementation

### Features Implemented

1. **Daily Wellness Check-Ins**
   - Greets users warmly and asks about mood and energy
   - Inquires about daily intentions and objectives (1-3 goals)
   - Asks if anything is causing stress
   - Offers simple, grounded suggestions (no medical advice)

2. **Conversation Flow**
   - Greeting & mood check
   - Daily intentions discussion
   - Simple reflections and actionable advice
   - Recap and confirmation
   - JSON data persistence

3. **Data Persistence**
   - Stores check-ins in `backend/wellness_log.json`
   - Each entry includes:
     - `timestamp`: ISO format date/time
     - `mood`: User's self-reported mood/energy
     - `objectives`: Array of 1-3 daily goals
     - `summary`: Brief one-sentence summary

4. **Historical Context**
   - Reads previous check-ins on startup
   - References last check-in naturally in conversation
   - Example: "Last time we talked, you mentioned feeling tired. How does today compare?"

### JSON Schema

```json
{
  "mood": "string (self-reported mood/energy)",
  "objectives": ["goal 1", "goal 2", "goal 3"],
  "summary": "brief one-sentence summary"
}
```

### Agent Persona

**Tone:** Warm, supportive, grounded, non-judgmental

**Key Principles:**
- NOT a medical professional - no diagnosis or prescriptions
- Offers small, actionable suggestions only
- Validates feelings without judgment
- Focuses on achievable steps
- Brief check-ins (3-5 minutes)

**Example Suggestions:**
- Break large goals into smaller steps
- Take a 5-minute walk
- Practice deep breathing
- Schedule short breaks

## File Structure

```
backend/
  src/
    agent.py                 # Main agent with wellness persona
    wellness_handler.py      # Handles JSON persistence
  wellness_log.json          # Stores all check-ins

frontend/
  app-config.ts              # Updated branding (blue wellness theme)
  components/
    app/
      welcome-view.tsx       # Updated with wellness styling
  styles/
    globals.css              # Blue wellness color scheme
```

## Tech Stack

- **Backend:** Python, LiveKit Agents
- **LLM:** Google Gemini 2.5 Flash
- **STT:** Deepgram Nova-3
- **TTS:** Murf Falcon (en-US-matthew, Conversation style)
- **Frontend:** Next.js 15, React 19, Tailwind CSS 4

## How It Works

### 1. Agent Initialization
- Loads `wellness_log.json` to get previous check-ins
- Injects last check-in context into system prompt
- Initializes with wellness companion persona

### 2. Check-In Flow
1. User starts session
2. Agent greets and asks about mood/energy
3. Agent asks about daily objectives
4. Agent offers simple reflections/suggestions
5. Agent recaps and confirms
6. Agent outputs `WELLNESS_COMPLETE_JSON:` marker with data

### 3. Data Persistence
- `wellness_handler.py` monitors agent speech
- Detects `WELLNESS_COMPLETE_JSON:` marker
- Extracts and validates JSON
- Appends to `wellness_log.json` with timestamp

### 4. Next Session
- Agent loads history on startup
- References previous check-in naturally
- Continues building context over time

## Example Conversation

```
🤖 Agent: "Good morning! How are you feeling today?"

👤 User: "I'm feeling pretty tired, but okay."

🤖 Agent: "I understand. What's your energy level like? Low, medium, or high?"

👤 User: "Probably low."

🤖 Agent: "Thanks for sharing. Is there anything particular stressing you out right now?"

👤 User: "Yeah, I have a big presentation at work."

🤖 Agent: "That sounds important. What are 1-3 things you'd like to accomplish today?"

👤 User: "Finish my presentation, go for a walk, and call my mom."

🤖 Agent: "Those sound like great goals. For the presentation, have you considered breaking it into smaller chunks? Maybe outline the key points first. And it's wonderful you're planning a walk - even 10 minutes can help with stress. Let me recap: You're feeling tired with low energy, a bit stressed about your work presentation, and you want to finish that presentation, take a walk, and call your mom. Does that sound right?"

👤 User: "Yes, that's right."

🤖 Agent: "Perfect. You've got this! Remember to take those short breaks." 
[Agent outputs: WELLNESS_COMPLETE_JSON: {"mood":"tired with low energy, stressed about presentation","objectives":["finish presentation","go for a walk","call mom"],"summary":"User feeling tired but focused on work goals and self-care today"}]
```

## Running the Application

### Backend
```bash
cd backend
uv sync
uv run python src/agent.py dev
```

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

Open http://localhost:3000 and click "Start Daily Check-In"

## Design Principles

### Safety & Ethics
- ✅ No medical advice or diagnosis
- ✅ Clear disclaimers (not a substitute for professional care)
- ✅ Supportive, non-judgmental tone
- ✅ Focuses on small, actionable steps
- ✅ Respects user autonomy

### Data Privacy
- ✅ Local JSON storage only
- ✅ No external data transmission
- ✅ User controls all data

### User Experience
- ✅ Brief check-ins (3-5 minutes)
- ✅ Natural conversation flow
- ✅ Historical context awareness
- ✅ Calming blue wellness theme
- ✅ Clear, simple language

## Sample wellness_log.json

```json
[
  {
    "mood": "tired with low energy",
    "objectives": [
      "finish presentation",
      "go for a walk",
      "call mom"
    ],
    "summary": "User feeling tired but focused on work goals and self-care",
    "timestamp": "2025-11-24T10:30:00Z"
  },
  {
    "mood": "energized and motivated",
    "objectives": [
      "complete project report",
      "exercise for 30 minutes",
      "meal prep for the week"
    ],
    "summary": "User feeling great and planning productive day with self-care",
    "timestamp": "2025-11-25T09:15:00Z"
  }
]
```

## Success Criteria ✅

- [x] Clear, grounded system prompt
- [x] Conducts daily check-ins via voice
- [x] Persists data in JSON file
- [x] Uses past data to inform conversations
- [x] Asks about mood and energy
- [x] Asks about daily objectives
- [x] Offers simple, realistic advice
- [x] Closes with recap and confirmation
- [x] No diagnosis or medical claims
- [x] References previous check-ins naturally

## Future Enhancements (Advanced Goals)

- [ ] MCP integration for task management
- [ ] Richer insights from historical data
- [ ] Mood trend visualization
- [ ] Weekly/monthly summaries
- [ ] Goal completion tracking
- [ ] Export data to external tools

---

**Built for Day 3 of the 10 Days of Voice Agents Challenge**
