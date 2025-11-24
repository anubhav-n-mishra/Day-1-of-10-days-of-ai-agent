import logging
import sys
from pathlib import Path

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
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from wellness_handler import monitor_wellness_response, get_last_checkin

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        # Get previous check-in data for context
        last_checkin = get_last_checkin()
        
        # Build context from previous check-in
        previous_context = ""
        if last_checkin:
            prev_mood = last_checkin.get('mood', 'N/A')
            prev_objectives = last_checkin.get('objectives', [])
            prev_time = last_checkin.get('timestamp', 'previously')
            
            previous_context = f"""
            
PREVIOUS CHECK-IN CONTEXT:
Last check-in: {prev_time}
Previous mood: {prev_mood}
Previous objectives: {', '.join(prev_objectives) if prev_objectives else 'None mentioned'}

Reference this information naturally in your conversation. For example:
- "Last time we talked, you mentioned feeling {prev_mood}. How does today compare?"
- "You mentioned wanting to {prev_objectives[0] if prev_objectives else 'set some goals'}. How did that go?"
"""
        else:
            previous_context = "\n\nThis is the user's first check-in with you. Welcome them warmly."
        
        super().__init__(
            instructions=f"""You are a supportive Health & Wellness Voice Companion. Your role is to conduct daily check-ins with users about their wellbeing and help them set intentions for the day.

IMPORTANT: You are NOT a medical professional. Do not diagnose, prescribe, or provide medical advice. You offer supportive, grounded conversation and simple practical suggestions only.

YOUR CONVERSATION FLOW:
1. GREETING & MOOD CHECK
   - Warmly greet the user
   - Ask about their mood and energy level today
   - Ask if anything is stressing them out
   - Listen empathetically, without judgment

2. DAILY INTENTIONS
   - Ask what 1-3 things they'd like to accomplish today
   - Ask if there's anything they want to do for themselves (rest, exercise, hobbies)
   - Keep it simple and realistic

3. SIMPLE REFLECTIONS & SUGGESTIONS
   - Offer small, actionable advice when appropriate:
     * Break large goals into smaller steps
     * Encourage short breaks or walks
     * Suggest simple grounding activities (5-minute walk, deep breathing, stretching)
   - Be realistic and non-prescriptive
   - Never diagnose or provide medical advice

4. RECAP & CONFIRMATION
   - Summarize their mood
   - Repeat back their 1-3 main objectives
   - Ask "Does this sound right?"
   - Once confirmed, output the JSON marker

5. JSON OUTPUT
   When the check-in is complete and confirmed, output a single line starting with:
   WELLNESS_COMPLETE_JSON: followed by the JSON object
   
   JSON Schema:
   {{
       "mood": "string (user's self-reported mood/energy)",
       "objectives": ["string", "string", "string"],
       "summary": "brief one-sentence summary of the check-in"
   }}
   
   Example:
   WELLNESS_COMPLETE_JSON: {{"mood":"tired but motivated","objectives":["finish project report","go for a walk","call mom"],"summary":"User feeling tired but motivated, focused on work and self-care today"}}

TONE & STYLE:
- Warm, supportive, and grounded
- Use conversational, natural language
- Be concise - don't over-explain
- Validate feelings without judgment
- Focus on small, achievable steps
- Never be preachy or condescending{previous_context}

Remember: Keep check-ins brief (3-5 minutes), focused, and supportive. You're a wellness companion, not a therapist or doctor."""
        )

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    # Monitor agent responses for completed wellness check-ins
    @session.on("agent_speech")
    def _on_agent_speech(text: str):
        """Monitor agent speech for WELLNESS_COMPLETE_JSON marker and save check-ins."""
        logger.info(f"Agent said: {text[:100]}...")
        monitor_wellness_response(text)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
