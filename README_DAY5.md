# Day 5: SDR Lead Capture Agent - Razorpay

## 🎯 Primary Goal Complete

Built an AI-powered Sales Development Representative (SDR) agent for **Razorpay** that:
- ✅ Acts as a knowledgeable SDR named "Priya"
- ✅ Answers company/product/pricing questions using FAQ database
- ✅ Collects 7 key lead fields naturally during conversation
- ✅ Generates end-of-call summary and saves leads to JSON

---

## 🏢 Company Selected: Razorpay

**Why Razorpay?**
- Leading Indian fintech startup (Founded 2014, Bangalore)
- Comprehensive product portfolio (Payment Gateway, Business Banking, Capital)
- Clear use cases and pricing structure
- Trusted by 10+ million businesses in India

---

## 📋 Features Implemented

### 1. **Comprehensive FAQ Database** (`razorpay_faq.json`)
- Company information (founding, headquarters, tagline)
- 4 main products with detailed features:
  - Payment Gateway (100+ payment methods)
  - RazorpayX (Business Banking)
  - Razorpay Capital (Business Loans)
  - Payment Links (No-code solution)
- Pricing structure (transparent and volume-based)
- 12 common FAQs covering:
  - Product capabilities
  - Target audience
  - Integration difficulty
  - Security & compliance
  - Support & pricing

### 2. **Intelligent SDR Agent** (`agent.py`)

**Agent Persona: Priya**
- Voice: Murf Falcon Alicia (warm, professional female voice)
- Personality: Friendly, consultative, knowledgeable
- Goal: Build relationships while qualifying leads

**Conversation Flow:**
1. **Greeting**: Warm introduction as Razorpay SDR
2. **Discovery**: Asks about name, company, and needs
3. **Consultation**: Answers questions using FAQ database
4. **Lead Collection**: Naturally gathers qualification data
5. **Closing**: Summarizes call and confirms next steps

### 3. **Lead Collection System**

**7 Key Fields Collected:**
| Field | Purpose | Example |
|-------|---------|---------|
| Name | Personal identification | "Anubhav Mishra" |
| Company | Business context | "TechStartup India" |
| Email | Follow-up contact | "anubhav@techstartup.in" |
| Role | Decision-making authority | "Founder / CTO" |
| Use Case | Solution fit | "E-commerce payments" |
| Team Size | Business scale | "10-50 employees" |
| Timeline | Urgency level | "Immediately / Next month" |

**Tools Implemented:**
- `collect_lead_info()`: Stores information as it's gathered
- `end_call_summary()`: Generates verbal summary and saves to JSON

### 4. **Lead Storage** (`leads.json`)
Each lead saved with:
```json
{
  "name": "...",
  "company": "...",
  "email": "...",
  "role": "...",
  "use_case": "...",
  "team_size": "...",
  "timeline": "...",
  "timestamp": "2025-11-26T...",
  "call_id": "20251126_145320"
}
```

### 5. **Razorpay-Branded Frontend**

**Updated Components:**
- `app-config.ts`: Razorpay branding, "Connect with Priya" CTA
- `welcome-view.tsx`: 
  - Razorpay blue theme (#3395FF)
  - 3 feature cards (Payment Gateway, Business Banking, Instant Credit)
  - Trust indicators (10M+ businesses)
  - Professional SDR positioning
- `globals.css`: Razorpay color scheme throughout

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | LiveKit Agents 1.3.2 |
| **STT** | Deepgram Nova-3 |
| **LLM** | Google Gemini 2.5 Flash |
| **TTS** | Murf Falcon (Alicia voice) |
| **Turn Detection** | MultilingualModel |
| **Frontend** | Next.js 15, React 19, Tailwind CSS |
| **Storage** | JSON files (FAQ + Leads) |

---

## 🚀 How It Works

### Agent Behavior

1. **Greeting Phase**
   ```
   "Hello! I'm Priya from Razorpay. Thank you for connecting with us today! 
   Before we dive in, I'd love to learn more about you and your business. 
   May I know your name?"
   ```

2. **Discovery Phase**
   - Asks open-ended questions about their business
   - Listens for pain points and needs
   - Matches needs to Razorpay products

3. **Question Answering**
   - Uses FAQ database exclusively (no hallucination)
   - Provides specific, accurate information
   - Handles objections professionally

4. **Lead Qualification**
   - Collects information naturally throughout conversation
   - Uses `collect_lead_info` tool after each data point
   - Maintains conversational flow (not interrogative)

5. **Call Closing**
   ```
   "Perfect! Let me quickly summarize what we discussed today.
   
   I spoke with [Name] from [Company], who is a [Role]. They're interested 
   in using Razorpay for [Use Case]. Their team size is [Size], and they're 
   looking to implement this [Timeline].
   
   I have your email as [Email], and I'll send you detailed information..."
   ```

### FAQ Preloading

```python
def prewarm(proc: JobProcess):
    """Prewarm function to load FAQ content early."""
    proc.userdata["vad"] = silero.VAD.load()
    proc.userdata["faq_content"] = load_faq_content()
    logger.info("FAQ content preloaded successfully")
```

Benefits:
- Instant access to FAQ data
- No file I/O during conversations
- Faster response times

---

## 📊 Example Conversation Flow

**User:** "Hi, I'm looking for a payment solution for my e-commerce store."

**Priya:** "Hello! I'm Priya from Razorpay. Thank you for connecting! Before we dive in, may I know your name?"

**User:** "I'm Rahul."

**Priya:** "Great to meet you, Rahul! What company are you with, and what specifically are you looking for in a payment solution?"

**User:** "I run FashionHub India. We need to accept online payments."

**Priya:** "Perfect! Razorpay's Payment Gateway would be ideal for FashionHub India. We support 100+ payment methods including UPI, cards, net banking, and wallets, with 99.99% uptime. What's your role at FashionHub India?"

**User:** "I'm the founder."

**Priya:** "Wonderful! As a founder, you'll appreciate our instant settlements and easy integration. What's the best email to send you more details?"

*[Continues collecting use case, team size, timeline naturally...]*

**User:** "That's all I needed to know. Thanks!"

**Priya:** "Perfect! Let me quickly summarize... [provides summary] ... Thank you so much for your time today, Rahul! We're excited about the possibility of working with FashionHub India. Have a great day!"

---

## 🎯 Primary Goal Achievement Checklist

- ✅ **SDR Persona**: Agent clearly behaves as Razorpay SDR (Priya)
- ✅ **FAQ Answering**: Uses FAQ database to answer product/pricing questions
- ✅ **Lead Collection**: Politely asks for and stores 7 key lead fields
- ✅ **Natural Conversation**: Consultative, not robotic
- ✅ **Data Storage**: Saves leads to JSON with timestamp
- ✅ **Call Summary**: Generates verbal summary at end of call
- ✅ **Razorpay Branding**: Frontend matches company theme

---

## 🔧 Setup & Usage

### Backend Setup
```bash
cd backend
uv run --directory backend python src/agent.py dev
```

### Frontend Setup
```bash
cd frontend
pnpm dev
```

### Testing the Agent
1. Open browser to `http://localhost:3000`
2. Click "Connect with Priya"
3. Ask questions about Razorpay:
   - "What does Razorpay do?"
   - "Do you have a free tier?"
   - "How quickly do I get my money?"
4. Provide lead information when asked
5. Say "That's all, thanks!" to end the call
6. Check `backend/leads.json` for saved lead data

---

## 📁 File Structure

```
backend/
├── src/
│   └── agent.py              # Main SDR agent implementation
├── razorpay_faq.json          # FAQ database
└── leads.json                 # Collected leads storage

frontend/
├── app-config.ts              # Razorpay branding config
├── components/app/
│   └── welcome-view.tsx       # Razorpay-themed welcome screen
└── styles/
    └── globals.css            # Razorpay color scheme
```

---

## 🎨 UI Screenshots

**Welcome Screen:**
- Razorpay blue theme (#3395FF)
- 3 feature cards highlighting key products
- "Connect with Priya" call-to-action
- Trust badge (10M+ businesses)

**During Call:**
- Real-time transcript display
- Agent status indicators
- Microphone controls

---

## 💡 Key Learnings

1. **Conversational Lead Collection**: Natural flow > interrogation
2. **FAQ Preloading**: Significant performance improvement
3. **Tool-Based Data Collection**: Clean separation of concerns
4. **Persona Consistency**: Voice + instructions + branding = believable SDR
5. **Gemini for SDR**: Excellent at consultative selling with right prompts

---

## 🚀 Potential Enhancements (Advanced Goals)

### Not Implemented (Future Work):
- [ ] Mock meeting scheduler
- [ ] CRM-style call notes with qualification score
- [ ] Persona-aware pitching (developer vs founder)
- [ ] Follow-up email draft generation
- [ ] Return visitor recognition

---

## 📝 Day 5 Completion

**Status**: ✅ Primary Goal Complete

**What Was Built:**
- Razorpay SDR agent with natural lead collection
- Comprehensive FAQ system with 12+ questions covered
- Lead storage with all 7 key fields
- End-of-call summary generation
- Razorpay-branded frontend

**Ready For:**
- Video recording and demo
- LinkedIn post with #MurfAIVoiceAgentsChallenge
- Testing with real conversations

---

## 🙏 Acknowledgments

- **Murf AI** for Falcon TTS voices (Alicia as Priya)
- **Razorpay** for being an excellent Indian startup to showcase
- **LiveKit** for the agent framework
- **Day 5 Challenge** for the SDR concept

---

## 📧 Contact

**Agent Voice:** Priya (Murf Falcon Alicia)  
**Company:** Razorpay (Demo Implementation)  
**Challenge:** #10DaysOfAIVoiceAgents - Day 5  
**Branch:** `SDR-Lead-Capture`
