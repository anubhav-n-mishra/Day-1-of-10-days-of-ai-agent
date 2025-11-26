import logging
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Load PayFlow FAQ content
FAQ_PATH = Path(__file__).parent.parent / "payflow_faq.json"
LEADS_PATH = Path(__file__).parent.parent / "leads.json"

def load_faq_content():
    """Load the FAQ content from JSON file."""
    with open(FAQ_PATH, 'r') as f:
        return json.load(f)

def save_lead(lead_data: Dict):
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
