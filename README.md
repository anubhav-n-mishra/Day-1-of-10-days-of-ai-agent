# AI Voice Agents Challenge - Starter Repository (Day 1)

Welcome to the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai)!

This copy of the starter repository has been set up and tested by **Anubhav Mishra** for Day 1 of the challenge.
Repository: https://github.com/anubhav-n-mishra/Day-1-of-10-days-of-ai-agent

## About the Challenge

We just launched **Murf Falcon** – the consistently fastest TTS API, and you're going to be among the first to test it out in ways never thought before!

**Build 10 AI Voice Agents over the course of 10 Days** along with help from our devs and the community champs, and win rewards!

### How It Works

- One task to be provided everyday along with a GitHub repo for reference
- Build a voice agent with specific personas and skills
- Post on GitHub and share with the world on LinkedIn!

## Repository Structure

This is a **monorepo** that contains both the backend and frontend for building voice agent applications. It's designed to be your starting point for each day's challenge task.

```
falcon-tdova-nov25-livekit/
├── backend/          # LiveKit Agents backend with Murf Falcon TTS
├── frontend/         # React/Next.js frontend for voice interaction
├── start_app.sh      # Convenience script to start all services
└── README.md         # This file
```

### Backend

The backend is based on [LiveKit's agent-starter-python](https://github.com/livekit-examples/agent-starter-python) with modifications to integrate **Murf Falcon TTS** for ultra-fast, high-quality voice synthesis.

**Features:**

- Complete voice AI agent framework using LiveKit Agents
- Murf Falcon TTS integration for fastest text-to-speech
- LiveKit Turn Detector for contextually-aware speaker detection
- Background voice cancellation
- Integrated metrics and logging
- Complete test suite with evaluation framework
- Production-ready Dockerfile

[→ Backend Documentation](./backend/README.md)

### Frontend

The frontend is based on [LiveKit's agent-starter-react](https://github.com/livekit-examples/agent-starter-react), providing a modern, beautiful UI for interacting with your voice agents.

**Features:**

- Real-time voice interaction with LiveKit Agents
- Camera video streaming support
- Screen sharing capabilities
- Audio visualization and level monitoring
- Light/dark theme switching
- Highly customizable branding and UI

[→ Frontend Documentation](./frontend/README.md)

## Quick Start

### Prerequisites

Make sure you have the following installed:

- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- [LiveKit CLI](https://docs.livekit.io/home/cli/cli-setup) (optional but recommended)
- [LiveKit Server](https://docs.livekit.io/home/self-hosting/local/) for local development

### 1. Clone the Repository

From your machine (example using the repo created for Day 1):

```powershell
git clone https://github.com/anubhav-n-mishra/Day-1-of-10-days-of-ai-agent.git
cd Day-1-of-10-days-of-ai-agent
```

### 2. Backend Setup (Windows PowerShell)

Open a PowerShell terminal and run the following (these are the exact commands used during Day 1 setup):

```powershell
cd .\backend

# Create sync the dependencies and virtual environment (uses uv package manager)
python -m uv sync

# Copy the example env file and edit it with your provider keys (do NOT commit secrets)
Copy-Item .env.example .env.local
# Edit backend/.env.local and fill: LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, MURF_API_KEY, GOOGLE_API_KEY, DEEPGRAM_API_KEY

# (optional) Download required model/assets used by the agent
python -m uv run python src/agent.py download-files

# Start the backend agent (use the venv Python to avoid multiprocessing issues on Windows)
.\.venv\Scripts\python.exe src/agent.py dev
```

For LiveKit Cloud users, you can automatically populate credentials:

```bash
lk cloud auth
lk app env -w -d .env.local
```

### 3. Frontend Setup (Windows PowerShell)

In a separate PowerShell terminal run:

```powershell
cd .\frontend

# Install dependencies
pnpm install

# Copy example env and add LiveKit credentials (same as backend)
Copy-Item .env.example .env.local
# Edit frontend/.env.local: LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET

# Start the dev server
pnpm dev
```

### 4. Run the Application

#### Install livekit server

```bash
brew install livekit
```

You have two options:

#### Option A: Use the convenience script (runs everything)

```bash
# From the root directory
chmod +x start_app.sh
./start_app.sh
```

This will start:

- LiveKit Server (in dev mode)
- Backend agent (listening for connections)
- Frontend app (at http://localhost:3000)

#### Option B: Run services individually (Windows notes)

If you prefer to run services manually:

1) LiveKit Server (optional - you can also use LiveKit Cloud):

```powershell
# Run LiveKit server locally (use Docker or the binary per LiveKit docs)
livekit-server --dev
```

2) Backend (use venv Python as shown above):

```powershell
cd backend
.\.venv\Scripts\python.exe src/agent.py dev
```

3) Frontend (run in another terminal):

```powershell
cd frontend
pnpm dev
```

Open `http://localhost:3001` (Next may choose 3001 if 3000 is in use).

Note: Browsers only allow microphone/camera access on secure contexts — `localhost` is accepted; accessing the frontend by raw LAN IP (e.g. `192.168.x.x`) will trigger media device errors unless served over HTTPS or via a secure tunnel like `ngrok`.

## Daily Challenge Tasks

Each day, you'll receive a new task that builds upon your voice agent. The tasks will help you:

- Implement different personas and conversation styles
- Add custom tools and capabilities
- Integrate with external APIs
- Build domain-specific agents (customer service, tutoring, etc.)
- Optimize performance and user experience

**Stay tuned for daily task announcements!**

## Documentation & Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Original Backend Template](https://github.com/livekit-examples/agent-starter-python)
- [Original Frontend Template](https://github.com/livekit-examples/agent-starter-react)

## Testing

The backend includes a comprehensive test suite:

```bash
cd backend
uv run pytest
```

Learn more about testing voice agents in the [LiveKit testing documentation](https://docs.livekit.io/agents/build/testing/).

## Contributing & Community

This is a challenge repository, but we encourage collaboration and knowledge sharing!

- Share your solutions and learnings on GitHub
- Post about your progress on LinkedIn
- Join the [LiveKit Community Slack](https://livekit.io/join-slack)
- Connect with other challenge participants

## License

## Day 2 — Coffee Shop Barista (What I implemented)

For Day 2 of the challenge I converted the starter agent into a friendly coffee shop barista. What I implemented locally in this copy:

- Barista persona and behavior inside `backend/src/agent.py` (assistant prompts and behavior updated).
- The assistant is instructed to output a single-line marker when the order is complete:
	- `ORDER_COMPLETE_JSON: { ... }` (the agent will print a single line that begins with that token and contains the final JSON order).
- A helper script `backend/save_order.py` was added to persist orders to `backend/orders.json` when you supply the JSON to the script.

Quick test and save workflow (manual save):

1. Start backend (use venv Python to avoid Windows multiprocessing issues):

```powershell
cd backend
.\.venv\Scripts\python.exe src/agent.py dev
```

2. Start frontend in another terminal:

```powershell
cd frontend
pnpm dev
```

3. Open `http://localhost:3001` (or `http://localhost:3000`) and place a coffee order by speaking to the agent.

4. When the agent completes the order it will output a single line starting with `ORDER_COMPLETE_JSON:`. Copy the JSON object that follows and run:

```powershell
python .\backend\save_order.py '{"drinkType":"latte","size":"medium","milk":"oat","extras":["vanilla"],"name":"Alex"}'
```

This will append the order to `backend/orders.json`.

If you want fully automatic saving (agent writes the file itself), I can implement a small handler that watches assistant output server-side and invokes the same save logic automatically — tell me if you want that next.

## License

This repository copy (Day 1 starter + my local changes) is released under the MIT License. See the root `LICENSE` file for details.

Original templates and third-party components may have their own licenses — see `backend/LICENSE` and `frontend/LICENSE` files where applicable.

## Have Fun!

Remember, the goal is to learn, experiment, and build amazing voice AI agents. Don't hesitate to be creative and push the boundaries of what's possible with Murf Falcon and LiveKit!

Good luck with the challenge!

---

Built for the AI Voice Agents Challenge by murf.ai
