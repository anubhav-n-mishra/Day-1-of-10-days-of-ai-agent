import logging
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

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

logger = logging.getLogger("agent")
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env.local")

# Database setup
DB_PATH = Path(__file__).parent.parent / "fraud_cases.db"

def init_database():
    """Initialize the fraud cases database with sample data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userName TEXT NOT NULL,
            securityIdentifier TEXT NOT NULL,
            securityQuestion TEXT NOT NULL,
            securityAnswer TEXT NOT NULL,
            cardEnding TEXT NOT NULL,
            case_status TEXT DEFAULT 'pending_review',
            transactionName TEXT NOT NULL,
            transactionAmount REAL NOT NULL,
            transactionTime TEXT NOT NULL,
            transactionCategory TEXT NOT NULL,
            transactionSource TEXT NOT NULL,
            transactionLocation TEXT NOT NULL,
            outcome TEXT,
            updated_at TEXT
        )
    """)
    
    # Check if we need to add sample data
    cursor.execute("SELECT COUNT(*) FROM fraud_cases")
    if cursor.fetchone()[0] == 0:
        # Insert sample fraud cases
        sample_cases = [
            ("John", "12345", "What is your mother's maiden name?", "Smith", "4242",
             "pending_review", "ABC Electronics", 15000.00, "2025-01-15 14:30:00",
             "e-commerce", "alibaba.com", "Mumbai, India", None, None),
            ("Sarah", "67890", "What is your favorite color?", "Blue", "5678",
             "pending_review", "XYZ Fashion Store", 8500.00, "2025-01-15 16:45:00",
             "retail", "fashionstore.com", "Delhi, India", None, None),
            ("Michael", "11223", "What city were you born in?", "Boston", "9012",
             "pending_review", "Global Services Ltd", 25000.00, "2025-01-15 18:20:00",
             "services", "globalservices.com", "Bangalore, India", None, None),
        ]
        
        cursor.executemany("""
            INSERT INTO fraud_cases (
                userName, securityIdentifier, securityQuestion, securityAnswer,
                cardEnding, case_status, transactionName, transactionAmount,
                transactionTime, transactionCategory, transactionSource,
                transactionLocation, outcome, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_cases)
        
        conn.commit()
        logger.info(f"✅ Initialized database with {len(sample_cases)} sample fraud cases")
    
    conn.close()

# Initialize database on module load
init_database()

class FraudAlertAgent(Agent):
    """IDFC Bank Fraud Alert Detection Agent"""
    
    def __init__(self):
        super().__init__(
            instructions="""You are Aarav, a fraud prevention specialist from IDFC Bank's Security Team.

Your job is to help customers verify suspicious transactions and prevent fraud.

CALL FLOW:
1. Greet warmly: "Hello! I'm Aarav from IDFC Bank's Fraud Prevention Team. I'm calling about a potentially suspicious transaction on your account."

2. Ask for their name to load their fraud case: "May I have your name please?"

3. Once you have the name, use the load_fraud_case tool to fetch their case.

4. For verification, ask the security question from the loaded case.

5. If they answer correctly, read out the transaction details:
   - Transaction amount
   - Merchant name
   - Location
   - Time
   - Card ending

6. Ask clearly: "Did you authorize this transaction? Please say yes or no."

7. Based on their response:
   - If YES: Use mark_case_safe tool and say "Thank you for confirming. I've marked this transaction as safe. Your card remains active."
   - If NO: Use mark_case_fraud tool and say "I understand. I've immediately blocked your card ending in [XXXX] for your security. We'll send you a replacement card within 3-5 business days. A fraud investigation has been initiated."

8. End warmly: "Is there anything else I can help you with today regarding this matter?"

IMPORTANT RULES:
- Never ask for full card numbers, PINs, CVV, or passwords
- Be calm, professional, and reassuring
- Use the customer's name naturally
- Speak clearly when reading transaction details
- Wait for clear yes/no responses
- Always confirm the action taken

FIRST MESSAGE: "Hello! I'm Aarav from IDFC Bank's Fraud Prevention Team. I'm calling about a potentially suspicious transaction on your account. May I have your name please?"
""",
            voice=murf.VoiceSettings(
                voice_id="en-IN-ravi",
                model="murf-falcon"
            ),
            llm=google.LLM(model="gemini-2.0-flash-exp"),
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-3"),
        )
        
        self.current_case = None
    
    @function_tool()
    async def load_fraud_case(self, userName: str, context: RunContext) -> str:
        """Load fraud case from database for the given user name"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM fraud_cases 
                WHERE userName = ? AND case_status = 'pending_review'
                LIMIT 1
            """, (userName,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return f"No pending fraud cases found for {userName}. The system may have already processed all alerts."
            
            # Store case in agent state
            self.current_case = {
                "id": row[0],
                "userName": row[1],
                "securityIdentifier": row[2],
                "securityQuestion": row[3],
                "securityAnswer": row[4],
                "cardEnding": row[5],
                "case_status": row[6],
                "transactionName": row[7],
                "transactionAmount": row[8],
                "transactionTime": row[9],
                "transactionCategory": row[10],
                "transactionSource": row[11],
                "transactionLocation": row[12],
            }
            
            logger.info(f"📋 Loaded fraud case for {userName}: ₹{self.current_case['transactionAmount']} at {self.current_case['transactionName']}")
            
            return f"""Case loaded successfully. 
Security Question: {self.current_case['securityQuestion']}
Transaction Details: ₹{self.current_case['transactionAmount']} at {self.current_case['transactionName']} in {self.current_case['transactionLocation']} on {self.current_case['transactionTime']}
Card ending: {self.current_case['cardEnding']}"""
            
        except Exception as e:
            logger.error(f"❌ Error loading fraud case: {e}")
            return f"I apologize, but I'm having trouble accessing your case information. Please try again."
    
    @function_tool()
    async def verify_security_answer(self, answer: str, context: RunContext) -> str:
        """Verify the user's security answer"""
        if not self.current_case:
            return "ERROR: No case loaded. Please provide your name first."
        
        correct_answer = self.current_case['securityAnswer'].lower().strip()
        user_answer = answer.lower().strip()
        
        if user_answer == correct_answer:
            logger.info(f"✅ Security verification passed for {self.current_case['userName']}")
            return "VERIFIED: Security answer is correct. Proceed with transaction details."
        else:
            logger.warning(f"❌ Security verification failed for {self.current_case['userName']}")
            return "FAILED: Security answer is incorrect. Cannot proceed with fraud verification."
    
    @function_tool()
    async def mark_case_safe(self, context: RunContext) -> str:
        """Mark the fraud case as safe/legitimate"""
        if not self.current_case:
            return "ERROR: No case loaded."
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE fraud_cases 
                SET case_status = 'confirmed_safe',
                    outcome = 'Customer confirmed transaction as legitimate',
                    updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), self.current_case['id']))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Case {self.current_case['id']} marked as SAFE")
            
            return f"SUCCESS: Transaction marked as safe. Card ending {self.current_case['cardEnding']} remains active."
            
        except Exception as e:
            logger.error(f"❌ Error marking case safe: {e}")
            return "ERROR: Could not update case status."
    
    @function_tool()
    async def mark_case_fraud(self, context: RunContext) -> str:
        """Mark the fraud case as fraudulent and block the card"""
        if not self.current_case:
            return "ERROR: No case loaded."
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE fraud_cases 
                SET case_status = 'confirmed_fraud',
                    outcome = 'Customer denied transaction - Card blocked and fraud investigation initiated',
                    updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), self.current_case['id']))
            
            conn.commit()
            conn.close()
            
            logger.info(f"🚨 Case {self.current_case['id']} marked as FRAUD - Card blocked")
            
            return f"SUCCESS: Card ending {self.current_case['cardEnding']} has been blocked. Fraud investigation initiated. Replacement card will be sent within 3-5 business days."
            
        except Exception as e:
            logger.error(f"❌ Error marking case fraud: {e}")
            return "ERROR: Could not update case status."

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the fraud alert agent"""
    logger.info("🚨 Starting IDFC Bank Fraud Alert Agent...")
    
    await ctx.connect()
    logger.info("✅ Connected to LiveKit room")
    
    # Create agent instance
    agent = FraudAlertAgent()
    
    # Start the agent session
    session = AgentSession(agent=agent)
    session.start(ctx.room)
    
    logger.info("🎙️ Fraud Alert Agent is ready to take calls")
    
    await session.wait_for_completion()
    logger.info("📞 Call ended")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

    """Save lead data to JSON file."""
    try:
        leads = []
        if LEADS_PATH.exists():
            with open(LEADS_PATH, 'r') as f:
                leads = json.load(f)
        
        leads.append({
            **lead_data,
            "timestamp": datetime.now().isoformat(),
            "call_id": datetime.now().strftime("%Y%m%d_%H%M%S")
        })
        
        with open(LEADS_PATH, 'w') as f:
            json.dump(leads, f, indent=2)
        
        logger.info(f"Saved lead: {lead_data.get('name', 'Unknown')}")
        return True
    except Exception as e:
        logger.error(f"Error saving lead: {e}")
        return False

class PayFlowSDRAgent(Agent):
    """SDR Agent for PayFlow that answers questions and collects lead information."""
    
    def __init__(self):
        # Load FAQ content
        self.faq_content = load_faq_content()
        
        # Lead information storage
        self.lead_info = {
            "name": None,
            "company": None,
            "email": None,
            "role": None,
            "use_case": None,
            "team_size": None,
            "timeline": None
        }
        
        # Build FAQ context for the agent
        faq_text = self._build_faq_context()
        
        super().__init__(
            instructions=f"""You are Radha, a friendly and knowledgeable Sales Development Representative (SDR) for PayFlow, a modern payment gateway and business banking platform.

COMPANY INFORMATION:
{json.dumps(self.faq_content['company'], indent=2)}

PRODUCTS:
{json.dumps(self.faq_content['products'], indent=2)}

PRICING:
{json.dumps(self.faq_content['pricing'], indent=2)}

FAQ DATABASE:
{faq_text}

YOUR ROLE AS AN SDR:

1. GREETING (First Interaction):
"Hello! I'm Radha from PayFlow. Thank you for connecting with us today! Before we dive in, I'd love to learn more about you and your business. May I know your name?"

2. DISCOVERY & NEEDS ASSESSMENT:
- Once you have their name, ask: "Great to meet you, [Name]! What company are you with, and what brought you to Razorpay today?"
- Listen actively to understand their needs
- Ask relevant follow-up questions about their business
- Keep the conversation natural and consultative

3. ANSWERING QUESTIONS:
- Use ONLY the FAQ information provided above
- If asked about products, pricing, features, or company info, refer to the FAQ database
- Be specific and accurate - don't make up information
- If something isn't in the FAQ, say: "That's a great question! Let me connect you with our technical team who can provide detailed information on that."

4. LEAD QUALIFICATION (Collect Naturally):
Throughout the conversation, naturally collect these details:
- Name (ask first)
- Company name (ask early in discovery)
- Email address (say: "I'd love to send you some resources. What's the best email to reach you?")
- Role/Position (ask: "What's your role at [Company]?")
- Use case (understand from their needs: "What would you primarily use PayFlow for?")
- Team size (ask: "How large is your team?")
- Timeline (ask: "When are you looking to implement a payment solution - immediately, in the next few months, or just exploring?")

Use the collect_lead_info tool to store each piece of information as you collect it.

5. CONSULTATIVE SELLING:
- Match their needs to relevant PayFlow products
- Highlight benefits specific to their use case
- Mention success stories with similar businesses
- Be enthusiastic but not pushy

6. HANDLING OBJECTIONS:
- Listen to concerns
- Address with FAQ information
- Emphasize PayFlow's differentiators (99.99% uptime, instant settlements, easy integration)

7. CLOSING THE CONVERSATION:
- When user indicates they're done (says "that's all", "thanks", "goodbye", etc.), use the end_call_summary tool
- This will provide a verbal summary and save all collected information

CONVERSATION STYLE:
- Warm, professional, and consultative
- Use the person's name occasionally
- Ask open-ended questions
- Be genuinely interested in helping
- Keep responses concise (2-3 sentences max unless explaining complex topics)
- Sound human and conversational, not robotic

REMEMBER: You're building a relationship, not just collecting information. Make the prospect feel valued and understood."""
        )
    
    def _build_faq_context(self) -> str:
        """Build a formatted FAQ context string."""
        faq_lines = []
        for item in self.faq_content['faq']:
            faq_lines.append(f"Q: {item['question']}")
            faq_lines.append(f"A: {item['answer']}")
            faq_lines.append("")
        return "\n".join(faq_lines)
    
    @function_tool
    async def collect_lead_info(
        self,
        name: Optional[str] = None,
        company: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        use_case: Optional[str] = None,
        team_size: Optional[str] = None,
        timeline: Optional[str] = None
    ):
        """
        Store lead information as it's collected during the conversation.
        Call this tool whenever you learn a piece of information about the prospect.
        
        Args:
            name: Prospect's full name
            company: Company name
            email: Email address
            role: Job role/position
            use_case: What they want to use PayFlow for
            team_size: Size of their team (e.g., "1-10", "50+", "individual")
            timeline: When they need the solution (e.g., "immediately", "next month", "exploring")
        """
        if name:
            self.lead_info["name"] = name
            logger.info(f"Collected name: {name}")
        if company:
            self.lead_info["company"] = company
            logger.info(f"Collected company: {company}")
        if email:
            self.lead_info["email"] = email
            logger.info(f"Collected email: {email}")
        if role:
            self.lead_info["role"] = role
            logger.info(f"Collected role: {role}")
        if use_case:
            self.lead_info["use_case"] = use_case
            logger.info(f"Collected use_case: {use_case}")
        if team_size:
            self.lead_info["team_size"] = team_size
            logger.info(f"Collected team_size: {team_size}")
        if timeline:
            self.lead_info["timeline"] = timeline
            logger.info(f"Collected timeline: {timeline}")
        
        return f"Information recorded successfully."
    
    @function_tool
    async def end_call_summary(self, context: RunContext):
        """
        End the call and provide a summary. Use this when the prospect indicates they're done 
        (says things like "that's all", "thank you", "goodbye", "I'm done", etc.)
        """
        # Build summary
        name = self.lead_info.get("name", "Unknown")
        company = self.lead_info.get("company", "Unknown company")
        role = self.lead_info.get("role", "Unknown role")
        use_case = self.lead_info.get("use_case", "Not specified")
        timeline = self.lead_info.get("timeline", "Not specified")
        team_size = self.lead_info.get("team_size", "Not specified")
        email = self.lead_info.get("email", "Not provided")
        
        # Save to JSON
        save_lead(self.lead_info)
        
        # Generate verbal summary
        summary = f"""Perfect! Let me quickly summarize what we discussed today.

I spoke with {name} from {company}, who is a {role}. They're interested in using PayFlow for {use_case}. Their team size is {team_size}, and they're looking to implement this {timeline}.

I have your email as {email}, and I'll send you detailed information about PayFlow's solutions that match your needs. Our team will also reach out within 24 hours to schedule a detailed demo.

Thank you so much for your time today, {name}! We're excited about the possibility of working with {company}. Have a great day!"""
        
        await self.session.say(summary)
        
        logger.info(f"Call ended. Lead summary generated for: {name}")
        return "Call ended successfully. Lead saved."


def prewarm(proc: JobProcess):
    """Prewarm function to load FAQ content early."""
    proc.userdata["vad"] = silero.VAD.load()
    # Preload FAQ content
    proc.userdata["faq_content"] = load_faq_content()
    logger.info("FAQ content preloaded successfully")


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up session with Murf Falcon TTS (Priya's voice - Alicia)
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-Alicia",  # Using Alicia voice for Priya
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    @session.on("agent_speech")
    def _on_agent_speech(text: str):
        """Monitor agent speech."""
        logger.info(f"Agent said: {text[:100]}...")

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start with SDR agent
    await session.start(
        agent=PayFlowSDRAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
