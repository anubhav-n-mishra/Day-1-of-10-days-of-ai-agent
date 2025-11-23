# Starbucks Voice Barista - Day 2 Challenge

An AI-powered voice barista that takes coffee orders using natural language and saves them to JSON.

## 🎯 Features

- **Voice Ordering**: Natural conversation with AI barista
- **Order State Management**: Tracks drink type, size, milk, extras, and customer name
- **Automatic Persistence**: Orders automatically saved to `backend/orders.json`
- **Beautiful Starbucks UI**: Clean white design with signature green accents
- **Real-time Animations**: Pulse effects and status indicators during voice interaction

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+ with pnpm
- LiveKit API credentials
- Google Gemini API key
- Murf API key
- Deepgram API key

### Setup

1. **Backend Setup**
```powershell
cd backend
# Create .env.local with your API keys:
# LIVEKIT_URL=wss://...
# LIVEKIT_API_KEY=...
# LIVEKIT_API_SECRET=...
# GOOGLE_API_KEY=...
# GEMINI_API_KEY=...
# MURF_API_KEY=...
# DEEPGRAM_API_KEY=...

# Install dependencies and start
.\.venv\Scripts\python.exe src/agent.py dev
```

2. **Frontend Setup**
```powershell
cd frontend
# Create .env.local with LiveKit credentials

# Install and start
pnpm install
pnpm dev
```

3. **Access the App**
Open http://localhost:3002 (or whatever port Next.js assigns)

## 💬 Sample Conversation

```
Agent: Welcome! What can I get for you today?
User: I'd like a coffee please
Agent: Great! What size would you like?
User: Medium
Agent: And what type of milk?
User: Oat milk
Agent: Would you like any extras?
User: Vanilla syrup
Agent: Perfect! And may I have your name?
User: Alex
Agent: So that's a medium coffee with oat milk and vanilla for Alex. Is that correct?
User: Yes
Agent: Great! Your order is ready.
```

## 📋 Order JSON Format

Orders are saved to `backend/orders.json`:

```json
[
  {
    "timestamp": "2025-11-23T17:30:00.000Z",
    "drinkType": "latte",
    "size": "medium",
    "milk": "oat",
    "extras": ["vanilla"],
    "name": "Alex"
  }
]
```

## 🎨 Tech Stack

**Backend:**
- LiveKit Agents SDK (Python)
- Google Gemini 2.5 Flash (LLM)
- Murf Falcon TTS (Text-to-Speech)
- Deepgram Nova-3 (Speech-to-Text)
- Multilingual turn detection

**Frontend:**
- Next.js 15.5.2 with Turbopack
- React 19
- LiveKit Components
- Framer Motion (animations)
- Tailwind CSS 4
- Lucide React (icons)

## 🔧 How It Works

1. **Voice Input**: User speaks their order
2. **Speech Recognition**: Deepgram converts speech to text
3. **LLM Processing**: Gemini understands intent and asks clarifying questions
4. **Order State**: Agent maintains JSON order structure
5. **Order Completion**: When complete, agent outputs `ORDER_COMPLETE_JSON:` marker
6. **Auto-Save**: `order_handler.py` detects marker and saves to `orders.json`
7. **Voice Output**: Murf converts text to natural speech

## 📁 Project Structure

```
├── backend/
│   ├── src/
│   │   ├── agent.py          # Main agent logic with barista persona
│   │   └── order_handler.py   # Order detection and JSON persistence
│   └── orders.json           # Saved orders (auto-created)
├── frontend/
│   ├── components/
│   │   ├── coffee/           # Coffee visualizer & status components
│   │   ├── app/              # Main app components
│   │   └── livekit/          # LiveKit UI components
│   ├── app/                  # Next.js app router
│   └── styles/               # Starbucks-themed CSS
└── challenges/
    └── Day 2 Task.md         # Original challenge requirements
```

## 🎯 Challenge Requirements Met

- ✅ Barista persona implemented
- ✅ Order state management (JSON schema)
- ✅ Clarifying questions until complete
- ✅ Automatic order persistence to JSON file
- ✅ Beautiful Starbucks-inspired UI
- ✅ Voice interaction with animations
- ✅ Clean project structure

## 🐛 Troubleshooting

**Agent not responding:**
- Check backend logs for errors
- Verify all API keys in `backend/.env.local`
- Ensure Python virtual environment is activated

**Frontend not loading:**
- Check `frontend/.env.local` has LiveKit credentials
- Verify port 3002 (or assigned port) is accessible
- Check browser console for errors

**Orders not saving:**
- Check backend logs for "Order saved successfully" message
- Verify write permissions in backend directory
- Check `backend/orders.json` is being created

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Anubhav Mishra
- GitHub: [@anubhav-n-mishra](https://github.com/anubhav-n-mishra)
- Repo: [Day-1-of-10-days-of-ai-agent](https://github.com/anubhav-n-mishra/Day-1-of-10-days-of-ai-agent)
- Branch: `coffee_barista`
