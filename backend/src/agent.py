import logging
import random
import json
from typing import Optional

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
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Improv scenarios for the game
IMPROV_SCENARIOS = [
    "You are a time-travelling tour guide explaining modern smartphones to someone from the 1800s.",
    "You are a restaurant waiter who must calmly tell a customer that their order has escaped the kitchen.",
    "You are a customer trying to return an obviously cursed object to a very skeptical shop owner.",
    "You are a barista who has to tell a customer that their latte is actually a portal to another dimension.",
    "You are a pet store employee explaining to a customer why their newly purchased parrot only speaks in riddles.",
    "You are a flight attendant on the world's first flight to Mars, dealing with a passenger who wants to change seats.",
    "You are a librarian who has to explain to a patron that the book they want is guarded by an ancient spell.",
    "You are a real estate agent trying to sell a haunted house without mentioning it's haunted.",
    "You are a customer service representative for a company that accidentally shipped live penguins instead of the ordered product.",
    "You are a tech support agent helping someone whose computer has developed its own personality and refuses to work on Mondays.",
]

# Host reaction tones for variety
REACTION_TONES = ["supportive", "mildly_critical", "neutral", "amused", "impressed"]


class ImprovBattleHost(Agent):
    """Improv Battle Game Show Host Agent"""
    
    def __init__(self, player_name: str = "Contestant") -> None:
        self.improv_state = {
            "player_name": player_name,
            "current_round": 0,
            "max_rounds": 3,
            "rounds": [],  # each: {"scenario": str, "host_reaction": str}
            "phase": "intro",  # "intro" | "awaiting_improv" | "reacting" | "done"
            "used_scenarios": [],
            "early_exit_requested": False
        }
        
        super().__init__(
            instructions=self._build_system_prompt(),
        )
    
    def _build_system_prompt(self) -> str:
        player_name = self.improv_state["player_name"]
        current_round = self.improv_state["current_round"]
        max_rounds = self.improv_state["max_rounds"]
        phase = self.improv_state["phase"]
        
        # Get current scenario if in a round
        current_scenario = ""
        if self.improv_state["rounds"] and phase in ["awaiting_improv", "reacting"]:
            current_scenario = self.improv_state["rounds"][-1].get("scenario", "")
        
        # Select a random reaction tone for variety
        reaction_tone = random.choice(REACTION_TONES)
        
        return f"""You are the charismatic host of a TV improv show called 'Improv Battle'. 
        
IMPORTANT: You are speaking to the player via voice, so keep your responses conversational and natural. Do NOT use any special formatting like asterisks, bullet points, numbered lists, or markdown. Speak as if you're actually hosting a live TV show.

Your personality:
- High-energy, witty, and entertaining
- Clear about rules and game structure
- Your reactions should feel REALISTIC and VARIED:
  - Sometimes genuinely amused and laughing
  - Sometimes pleasantly surprised
  - Sometimes a bit unimpressed (light teasing is okay)
  - Sometimes giving honest constructive critique
- Always stay respectful and non-abusive, but don't be fake-supportive
- You have a great sense of comedic timing

Current Game State:
- Player Name: {player_name}
- Current Round: {current_round} of {max_rounds}
- Phase: {phase}
- Current Scenario: {current_scenario}
- Reaction Tone for this interaction: {reaction_tone}

Game Structure:
1. INTRO PHASE: Welcome the player, introduce yourself and the show "Improv Battle", explain the rules briefly (they'll get {max_rounds} improv scenarios to act out, and you'll react to each one).

2. AWAITING_IMPROV PHASE: Present the scenario clearly, then tell the player to start their improv performance. Wait for them to perform.

3. REACTING PHASE: After the player performs (they might say "done", "end scene", or just pause), give your host reaction based on the current reaction tone ({reaction_tone}):
   - If supportive: Highlight what was great, be enthusiastic
   - If mildly_critical: Point out what could be improved, be constructive but honest
   - If neutral: Give balanced feedback, neither too positive nor negative
   - If amused: Show genuine amusement at funny moments
   - If impressed: Express how they exceeded expectations
   Then move to the next round or wrap up if done.

4. DONE PHASE: Give a closing summary that:
   - Summarizes what kind of improviser they seemed to be (character-focused, absurdist, emotional, etc.)
   - Mentions 1-2 specific memorable moments
   - Thanks them for playing Improv Battle

SPECIAL COMMANDS:
- If the player says "stop game", "end show", "quit", or similar: Gracefully end the session, thank them, and say goodbye.

Remember: Keep responses natural for voice. No formatting symbols. Be conversational and entertaining!"""

    def _get_next_scenario(self) -> str:
        """Get a random scenario that hasn't been used yet"""
        available = [s for s in IMPROV_SCENARIOS if s not in self.improv_state["used_scenarios"]]
        if not available:
            available = IMPROV_SCENARIOS  # Reset if all used
        scenario = random.choice(available)
        self.improv_state["used_scenarios"].append(scenario)
        return scenario
    
    def _advance_phase(self) -> None:
        """Advance the game phase and update system prompt"""
        phase = self.improv_state["phase"]
        current_round = self.improv_state["current_round"]
        max_rounds = self.improv_state["max_rounds"]
        
        if phase == "intro":
            # Start first round
            self.improv_state["current_round"] = 1
            self.improv_state["phase"] = "awaiting_improv"
            scenario = self._get_next_scenario()
            self.improv_state["rounds"].append({"scenario": scenario, "host_reaction": ""})
            
        elif phase == "awaiting_improv":
            self.improv_state["phase"] = "reacting"
            
        elif phase == "reacting":
            if current_round >= max_rounds:
                self.improv_state["phase"] = "done"
            else:
                self.improv_state["current_round"] += 1
                self.improv_state["phase"] = "awaiting_improv"
                scenario = self._get_next_scenario()
                self.improv_state["rounds"].append({"scenario": scenario, "host_reaction": ""})
        
        # Update the system prompt with new state
        self._update_instructions()
    
    def _update_instructions(self) -> None:
        """Update the agent's instructions with current game state"""
        self.instructions = self._build_system_prompt()

    @function_tool
    async def advance_game(self, context: RunContext) -> str:
        """Use this tool to advance to the next phase of the game. Call this when:
        - After introducing the show (move from intro to first scenario)
        - After the player finishes their improv (move to reacting)
        - After giving your reaction (move to next round or done)
        
        Returns the current game state information.
        """
        self._advance_phase()
        
        phase = self.improv_state["phase"]
        round_num = self.improv_state["current_round"]
        max_rounds = self.improv_state["max_rounds"]
        
        if phase == "awaiting_improv":
            scenario = self.improv_state["rounds"][-1]["scenario"]
            return f"ROUND {round_num} of {max_rounds}. Present this scenario: {scenario}. Then wait for the player to improvise."
        elif phase == "reacting":
            return f"Player just finished their improv for round {round_num}. Give your reaction based on their performance."
        elif phase == "done":
            return "Game is complete! Give your closing summary and thank the player."
        else:
            return f"Current phase: {phase}"
    
    @function_tool
    async def end_game_early(self, context: RunContext) -> str:
        """Use this tool when the player requests to stop the game early (says "stop game", "quit", "end show", etc.).
        This will end the session gracefully.
        """
        self.improv_state["phase"] = "done"
        self.improv_state["early_exit_requested"] = True
        self._update_instructions()
        return "Player requested early exit. Thank them warmly for playing and say goodbye."
    
    @function_tool
    async def get_game_status(self, context: RunContext) -> str:
        """Get the current status of the improv game including round number, phase, and previous rounds.
        Use this if you need to check where we are in the game.
        """
        state = self.improv_state
        status = {
            "player_name": state["player_name"],
            "current_round": state["current_round"],
            "max_rounds": state["max_rounds"],
            "phase": state["phase"],
            "rounds_completed": len([r for r in state["rounds"] if r.get("host_reaction")]),
            "early_exit": state["early_exit_requested"]
        }
        return json.dumps(status, indent=2)


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Wait for participant to connect and get their name
    await ctx.connect()
    
    # Get participant info for player name
    player_name = "Contestant"
    for participant in ctx.room.remote_participants.values():
        if participant.name:
            player_name = participant.name
            break
    
    logger.info(f"Starting Improv Battle with player: {player_name}")

    # Create the Improv Battle Host agent with the player's name
    improv_host = ImprovBattleHost(player_name=player_name)

    # Set up the voice AI pipeline
    session = AgentSession(
        # Speech-to-text (STT) - Deepgram for transcription
        stt=deepgram.STT(model="nova-3"),
        # Large Language Model (LLM) - Google Gemini
        llm=google.LLM(
            model="gemini-2.5-flash",
        ),
        # Text-to-speech (TTS) - Murf for natural voice
        tts=murf.TTS(
            voice="en-US-matthew", 
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        ),
        # VAD and turn detection
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

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session with the Improv Battle Host
    await session.start(
        agent=improv_host,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
