"""
agent_coordinator.py
────────────────────
Coordinator Agent – Routes questions to the correct specialized agent.

Architecture:
  1. User sends a question to the Coordinator.
  2. Coordinator sends the question + all 5 agent tool schemas to the LLM.
  3. LLM decides which agent tool to call (OpenAI function-calling format).
  4. Coordinator executes that agent locally and returns the answer.
  5. If the LLM cannot decide, the Coordinator falls back to the General Health Agent.
"""

import json
import logging
from openai import AsyncOpenAI

from config import API_URL, API_KEY, MODEL_NAME
from agents.agent_general        import GeneralHealthAgent
from agents.agent_sti            import STIAgent
from agents.agent_contraception  import ContraceptionAgent
from agents.agent_reproductive   import ReproductiveHealthAgent
from agents.agent_safety         import SafetyConsentAgent

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
#  Registry: name → agent instance
# ──────────────────────────────────────────────────────────────────────────────
AGENT_REGISTRY: dict[str, object] = {
    "general_health_agent"    : GeneralHealthAgent(),
    "sti_agent"               : STIAgent(),
    "contraception_agent"     : ContraceptionAgent(),
    "reproductive_health_agent": ReproductiveHealthAgent(),
    "safety_consent_agent"    : SafetyConsentAgent(),
}


# ──────────────────────────────────────────────────────────────────────────────
#  Coordinator
# ──────────────────────────────────────────────────────────────────────────────
class CoordinatorAgent:
    """
    Orchestrator that:
      • Holds references to all specialized agents.
      • Uses LLM function-calling to decide which agent handles a question.
      • Runs the chosen agent and returns its answer.
    """

    SYSTEM_PROMPT = """You are the coordinator of a sexual health virtual assistant.
You manage a team of 5 specialized agents. When the user asks a question,
you must call exactly ONE of the available tools that best matches the topic.

Agent overview:
- general_health_agent      → broad sexual health, hygiene, anatomy, wellness
- sti_agent                 → STIs/STDs (HIV, chlamydia, gonorrhea, herpes, HPV …)
- contraception_agent       → birth control, emergency contraception, family planning
- reproductive_health_agent → pregnancy, fertility, menstruation, PCOS, menopause …
- safety_consent_agent      → consent, healthy relationships, sexual violence, mental health

Rules:
1. Always call a tool – never answer directly without routing.
2. Pass the user's original question verbatim to the tool's `question` argument.
3. Choose the single most relevant agent.
4. If the question spans multiple topics, pick the PRIMARY topic.
"""

    def __init__(self):
        self.client  = AsyncOpenAI(
            base_url=API_URL,
            api_key=API_KEY if API_KEY else "no-key",
        )
        self.model   = MODEL_NAME
        self.agents  = AGENT_REGISTRY
        self.tools   = [agent.as_tool_schema() for agent in self.agents.values()]

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #
    async def run(self, question: str, chat_history: list[dict] | None = None) -> dict:
        """
        Route the user question to the best agent and return answer.
        """
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        if chat_history:
            messages.extend(chat_history)

        messages.append({"role": "user", "content": question})

        # ── Step 1: Ask the LLM to pick a tool ────────────────────────
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=256,
            )
        except Exception as exc:
            logger.error("Coordinator LLM call failed: %s", exc)
            return await self._fallback(question)

        choice = response.choices[0]

        # ── Step 2: Check if the LLM called a tool ────────────────────
        if choice.finish_reason != "tool_calls" or not choice.message.tool_calls:
            logger.warning("LLM did not call a tool; using fallback agent.")
            return await self._fallback(question)

        tool_call  = choice.message.tool_calls[0]
        agent_name = tool_call.function.name

        # Parse arguments
        try:
            args = json.loads(tool_call.function.arguments)
            routed_question = args.get("question", question)
        except (json.JSONDecodeError, AttributeError):
            routed_question = question

        # ── Step 3: Execute the chosen agent ──────────────────────────
        agent = self.agents.get(agent_name)
        if agent is None:
            logger.warning("Unknown agent %r; using fallback.", agent_name)
            return await self._fallback(question)

        answer = await agent.run(routed_question)

        return {
            "agent_used": agent_name,
            "question"  : question,
            "answer"    : answer,
        }

    async def get_route(self, question: str, chat_history: list[dict] | None = None) -> str:
        """
        Only decide which agent should handle the question.
        Used for streaming responses via WebSocket.
        """
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        if chat_history:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": question})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=256,
            )
            choice = response.choices[0]
            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                return choice.message.tool_calls[0].function.name
            return "general_health_agent"  # Fallback
        except Exception:
            return "general_health_agent"

    # ------------------------------------------------------------------ #
    #  Fallback                                                            #
    # ------------------------------------------------------------------ #
    async def _fallback(self, question: str) -> dict:
        """Use the general health agent when routing fails."""
        fallback_agent = self.agents["general_health_agent"]
        answer = await fallback_agent.run(question)
        return {
            "agent_used": "general_health_agent (fallback)",
            "question"  : question,
            "answer"    : answer,
        }

    # ------------------------------------------------------------------ #
    #  Utility                                                             #
    # ------------------------------------------------------------------ #
    def list_agents(self) -> list[dict]:
        """Return a summary list of all registered agents."""
        return [
            {"name": name, "description": agent.description}
            for name, agent in self.agents.items()
        ]