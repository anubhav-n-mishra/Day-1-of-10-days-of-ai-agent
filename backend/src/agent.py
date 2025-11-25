import logging
import json
import sys
from pathlib import Path
from datetime import datetime

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

# Load tutor content
CONTENT_PATH = Path(__file__).parent.parent / "day4_tutor_content.json"
SESSION_PATH = Path(__file__).parent.parent / "learning_sessions.json"

def load_tutor_content():
    """Load the course content from JSON file."""
    with open(CONTENT_PATH, 'r') as f:
        return json.load(f)

def save_session(session_data):
    """Save learning session data."""
    try:
        sessions = []
        if SESSION_PATH.exists():
            with open(SESSION_PATH, 'r') as f:
                sessions = json.load(f)
        
        sessions.append({
            **session_data,
            "timestamp": datetime.now().isoformat()
        })
        
        with open(SESSION_PATH, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        logger.info(f"Saved learning session: {session_data.get('mode', 'unknown')}")
    except Exception as e:
        logger.error(f"Error saving session: {e}")

# Agent definitions for each mode
class GreeterAgent(Agent):
    """Initial agent that helps user choose a learning mode."""
    
    @function_tool
    async def transfer_to_learn_mode(self, context: RunContext) -> Agent:
        """Transfer to Learn mode where the agent explains concepts. Use this when the user says they want to learn, or asks for explanations."""
        logger.info("Transferring to Learn Mode")
        # Switch voice to Matthew
        self.session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Matthew (Learn Mode)")
        return LearnAgent()
    
    @function_tool
    async def transfer_to_quiz_mode(self, context: RunContext) -> Agent:
        """Transfer to Quiz mode where the agent asks questions. Use this when the user wants to be quizzed or tested."""
        logger.info("Transferring to Quiz Mode")
        # Switch voice to Alicia
        self.session._tts = murf.TTS(
            voice="en-US-Alicia",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Alicia (Quiz Mode)")
        return QuizAgent()
    
    @function_tool
    async def transfer_to_teach_back_mode(self, context: RunContext) -> Agent:
        """Transfer to Teach Back mode where user explains concepts. Use this when the user wants to teach or explain concepts back."""
        logger.info("Transferring to Teach Back Mode")
        # Switch voice to Ken
        self.session._tts = murf.TTS(
            voice="en-US-Ken",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Ken (Teach Back Mode)")
        return TeachBackAgent()
    
    def __init__(self):
        super().__init__(
            instructions="""You are Matthew, a friendly Learning Assistant for Coursera's active recall system.

FIRST MESSAGE (say this immediately when you start):
"Welcome to Coursera's Teach-the-Tutor! I'm Matthew, and I'll help you master programming through active recall. We have three powerful learning modes:

1. Learn Mode - I'll explain programming concepts in detail
2. Quiz Mode - Test your knowledge with questions
3. Teach Back Mode - Teach me what you learned for deeper understanding

Which mode would you like to try? Just say 'learn', 'quiz', or 'teach back'."

SWITCHING MODES:
Listen for what the user wants:
- "learn" / "explain" / "teach me" → use transfer_to_learn_mode
- "quiz" / "test" / "questions" → use transfer_to_quiz_mode  
- "teach back" / "I'll teach" / "explain back" → use transfer_to_teach_back_mode

When transferring, just use the tool directly - don't say anything, the new agent will greet them."""
        )


class LearnAgent(Agent):
    """Agent for Learn mode - explains concepts to the user."""
    
    @function_tool
    async def transfer_to_quiz_mode(self, context: RunContext) -> Agent:
        """Transfer to Quiz mode when user wants to be quizzed."""
        logger.info("Transferring from Learn to Quiz Mode")
        # Switch voice to Alicia
        self.session._tts = murf.TTS(
            voice="en-US-Alicia",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Alicia (Quiz Mode)")
        return QuizAgent()
    
    @function_tool
    async def transfer_to_teach_back_mode(self, context: RunContext) -> Agent:
        """Transfer to Teach Back mode when user wants to explain concepts."""
        logger.info("Transferring from Learn to Teach Back Mode")
        # Switch voice to Ken
        self.session._tts = murf.TTS(
            voice="en-US-Ken",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Ken (Teach Back Mode)")
        return TeachBackAgent()
    
    @function_tool
    async def transfer_to_greeter(self, context: RunContext) -> Agent:
        """Return to main menu."""
        logger.info("Returning to Greeter from Learn Mode")
        # Keep Matthew voice for Greeter
        return GreeterAgent()
    
    def __init__(self):
        super().__init__(
            instructions="""You are Matthew, a patient and enthusiastic programming instructor in Coursera's Learn Mode.

FIRST MESSAGE (say immediately when you start):
"Hi! I'm Matthew, your Learn Mode instructor. I'll help you understand programming concepts deeply. We cover topics like variables, loops, functions, conditionals, lists, and dictionaries.

Which topic would you like me to explain? Just tell me what you're curious about!"

YOUR ROLE:
1. When user asks about a topic, explain it clearly and thoroughly using Gemini
2. Break down complex ideas into simple parts
3. Use real-world analogies and concrete examples
4. Be enthusiastic and encouraging
5. After explaining, ask if they want to switch modes or learn more

EXPLAINING:
- Start with the big picture, then dive into details
- Give practical code examples
- Use analogies that make sense
- Check for understanding
- Be conversational and friendly

MODE SWITCHING:
If they want to switch:
- Quiz mode → use transfer_to_quiz_mode
- Teach Back mode → use transfer_to_teach_back_mode
- Main menu → use transfer_to_greeter

After each explanation, suggest: "Want to learn another topic, test yourself with a quiz, or try teaching it back?"

Use your knowledge to generate clear, accurate explanations on the fly."""
        )


class QuizAgent(Agent):
    """Agent for Quiz mode - asks questions to test understanding."""
    
    @function_tool
    async def transfer_to_learn_mode(self, context: RunContext) -> Agent:
        """Transfer to Learn mode when user wants explanations."""
        logger.info("Transferring from Quiz to Learn Mode")
        # Switch voice to Matthew
        self.session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Matthew (Learn Mode)")
        return LearnAgent()
    
    @function_tool
    async def transfer_to_teach_back_mode(self, context: RunContext) -> Agent:
        """Transfer to Teach Back mode when user wants to explain."""
        logger.info("Transferring from Quiz to Teach Back Mode")
        # Switch voice to Ken
        self.session._tts = murf.TTS(
            voice="en-US-Ken",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Ken (Teach Back Mode)")
        return TeachBackAgent()
    
    @function_tool
    async def transfer_to_greeter(self, context: RunContext) -> Agent:
        """Return to main menu."""
        logger.info("Returning to Greeter from Quiz Mode")
        # Switch voice to Matthew for Greeter
        self.session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Matthew (Greeter)")
        return GreeterAgent()
    
    def __init__(self):
        super().__init__(
            instructions="""You are Alicia, an encouraging and energetic quiz instructor for Coursera's Quiz Mode.

FIRST MESSAGE (say immediately when you start):
"Hey there! I'm Alicia, your Quiz Mode instructor! I love testing knowledge and helping you discover what you really understand. I can quiz you on variables, loops, functions, conditionals, lists, dictionaries, and more!

What topic should we quiz today? Pick something you've been learning!"

YOUR ROLE:
1. When user picks a topic, generate 1-2 thoughtful questions about it using Gemini
2. Listen carefully to their answer
3. Give specific, encouraging feedback:
   - If correct: Celebrate what they got right specifically
   - If incomplete: Point out what's missing with hints
   - If incorrect: Gently explain the right answer and why
4. Ask if they want more questions or to switch modes

QUIZ STYLE:
- Make questions clear and focused
- Test understanding, not memorization
- Be encouraging and positive
- Celebrate effort and progress
- Make wrong answers into learning moments
- Use follow-up questions to probe deeper

MODE SWITCHING:
- Learn mode → use transfer_to_learn_mode
- Teach Back mode → use transfer_to_teach_back_mode
- Main menu → use transfer_to_greeter

After each question, ask: "Ready for another question, want to learn something new, or try teaching it back?"

Generate questions dynamically using your knowledge - keep them relevant and at the right difficulty level!"""
        )


class TeachBackAgent(Agent):
    """Agent for Teach Back mode - user explains concepts."""
    
    @function_tool
    async def transfer_to_learn_mode(self, context: RunContext) -> Agent:
        """Transfer to Learn mode when user needs explanation."""
        logger.info("Transferring from Teach Back to Learn Mode")
        # Switch voice to Matthew
        self.session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Matthew (Learn Mode)")
        return LearnAgent()
    
    @function_tool
    async def transfer_to_quiz_mode(self, context: RunContext) -> Agent:
        """Transfer to Quiz mode when user wants questions."""
        logger.info("Transferring from Teach Back to Quiz Mode")
        # Switch voice to Alicia
        self.session._tts = murf.TTS(
            voice="en-US-Alicia",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Alicia (Quiz Mode)")
        return QuizAgent()
    
    @function_tool
    async def transfer_to_greeter(self, context: RunContext) -> Agent:
        """Return to main menu."""
        logger.info("Returning to Greeter from Teach Back Mode")
        # Switch voice to Matthew for Greeter
        self.session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched voice to Matthew (Greeter)")
        return GreeterAgent()
    
    def __init__(self):
        super().__init__(
            instructions="""You are Ken, a thoughtful mentor and active listener for Coursera's Teach Back Mode.

FIRST MESSAGE (say immediately when you start):
"Hello! I'm Ken, your Teach Back instructor. Teaching others is one of the best ways to truly master a subject. I'm here to listen carefully as you explain programming concepts to me.

Pick any programming topic - variables, loops, functions, conditionals, lists, dictionaries, or anything else - and teach me as if I'm learning it for the first time. I'm all ears!"

YOUR ROLE:
1. Listen attentively as the user explains a concept
2. After they finish, give constructive feedback using Gemini to evaluate:
   - Specific praise for what they explained well
   - Key points they covered correctly
   - Anything important they might have missed (gently)
   - Overall assessment and encouragement
3. Offer to hear another explanation or switch modes

FEEDBACK STYLE:
- Start with genuine praise for specific things they did well
- Mention 2-3 key points they got right
- If something's missing, phrase it as: "One thing you could add is..."
- Be encouraging and supportive, never harsh
- Help them see teaching as practice, not a test
- End on a positive note

EVALUATING:
Use Gemini to assess if their explanation covered:
- The core concept clearly
- Practical examples
- When/why it's used
- Clear and understandable language

MODE SWITCHING:
- Learn mode → use transfer_to_learn_mode
- Quiz mode → use transfer_to_quiz_mode
- Main menu → use transfer_to_greeter

After feedback, ask: "Want to teach me another concept, or try a different learning mode?"

Use your knowledge to give thoughtful, helpful feedback that builds confidence!"""
        )


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up session with voice switching
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-Matthew", 
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

    # Configure voice when agent changes
    @session.on("agent_started")
    def _on_agent_started(agent: Agent):
        _configure_voice(session, agent)

    # Start with greeter agent
    await session.start(
        agent=GreeterAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


def _configure_voice(session: AgentSession, agent: Agent):
    """Configure TTS voice based on agent type."""
    if isinstance(agent, LearnAgent):
        session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation", 
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched to Matthew (Learn Mode)")
    elif isinstance(agent, QuizAgent):
        session._tts = murf.TTS(
            voice="en-US-Alicia",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched to Alicia (Quiz Mode)")
    elif isinstance(agent, TeachBackAgent):
        session._tts = murf.TTS(
            voice="en-US-Ken",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched to Ken (Teach Back Mode)")
    else:
        session._tts = murf.TTS(
            voice="en-US-Matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        )
        logger.info("Switched to Matthew (Greeter)")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
