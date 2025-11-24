# LinkedIn Post - Coffee Barista Voice Agent

---

🎙️ **Day 2 of Building AI Voice Agents: Coffee Shop Barista** ☕

Just completed Day 2 of the #10DaysOfVoiceAgents challenge, and I'm excited to share what I built!

**What I Created:**
A fully functional voice-powered coffee ordering system that acts as your personal Starbucks barista. Here's what makes it special:

✅ **Natural Conversation Flow**
- The AI asks clarifying questions until it has all order details
- Handles drink type, size, milk preferences, and extras
- Confirms the complete order before processing

✅ **Smart Order State Management**
- Maintains a structured JSON order schema
- Tracks: drinkType, size, milk, extras[], and customer name
- Automatically saves completed orders to orders.json

✅ **Starbucks-Inspired UI**
- Clean, professional design with authentic Starbucks green (#00704A)
- Animated coffee visualizer that pulses while listening
- Smooth transitions between welcome and ordering screens

✅ **Real-Time Voice Processing**
- Powered by LiveKit Agents framework
- Speech-to-Text: Deepgram Nova-3
- LLM: Google Gemini 2.5 Flash
- Text-to-Speech: Murf Falcon (natural voice)

**Sample Conversation:**
```
🤖 Barista: "Welcome! What can I get you today?"
👤 You: "I'd like a latte"
🤖 Barista: "Great! What size would you like?"
👤 You: "Large, with almond milk and vanilla syrup"
🤖 Barista: "Perfect! And what's the name for the order?"
👤 You: "John"
🤖 Barista: "Got it! One large latte with almond milk and vanilla syrup for John. I'll have that ready for you shortly!"
```

**Tech Stack:**
- Backend: Python, LiveKit Agents, Google Gemini
- Frontend: Next.js 15, React 19, Tailwind CSS 4
- Voice: Deepgram STT + Murf TTS + Multilingual Turn Detection

**Key Learnings:**
1. Voice agents need clear, structured prompts to maintain state
2. JSON output formatting requires careful token markers (ORDER_COMPLETE_JSON)
3. Real-time order persistence enables seamless handoffs
4. UI feedback is crucial for voice interactions

This was a significant step up from Day 1! Moving from a simple voice assistant to a stateful, domain-specific agent with order management.

**What's Next:**
Day 3 will explore more advanced agent capabilities. The journey from "Hello World" to production-ready voice commerce is fascinating!

💡 Interested in building voice AI? Check out the 10 Days of Voice Agents challenge by LiveKit!

#AI #VoiceAI #MachineLearning #LiveKit #Python #ReactJS #NextJS #Innovation #TechChallenge #DeveloperLife #BuildInPublic

---

🔗 GitHub: [Your Repo Link]
📹 [Optional: Demo Video Link]

---

**Image Suggestions for Post:**
1. Screenshot of the Starbucks-styled welcome screen
2. Screenshot of the active ordering session with coffee visualizer
3. Sample orders.json showing saved order data
4. Diagram showing the voice processing pipeline (STT → LLM → TTS)

---

**Alternative Shorter Version:**

☕ Built a voice-activated coffee ordering system today! 

My AI barista takes orders through natural conversation, maintains order state, and saves everything to JSON. Powered by LiveKit Agents + Google Gemini + Deepgram + Murf.

From "I'd like a latte" to complete order confirmation - all via voice! 🎙️

Day 2 of #10DaysOfVoiceAgents ✅

#VoiceAI #AI #BuildInPublic #TechChallenge

