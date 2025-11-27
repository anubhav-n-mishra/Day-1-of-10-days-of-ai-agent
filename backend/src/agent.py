import logging
import sqlite3
from pathlib import Path
from datetime import datetime

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
            tts=murf.TTS(voice="en-US-matthew", model="FALCON"),
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
    session = AgentSession()
    await session.start(agent, room=ctx.room)
    
    logger.info("🎙️ Fraud Alert Agent is ready to take calls")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
