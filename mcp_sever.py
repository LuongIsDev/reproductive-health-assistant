"""
mcp_server.py
─────────────
MCP (Model Context Protocol) Server
────────────────────────────────────
Exposes every specialized agent as an MCP tool, plus a coordinator tool
that auto-routes questions.

Run with:
    python mcp_server.py

Or as a module for Claude Desktop / any MCP host:
    {
        "mcpServers": {
            "sexual_health_bot": {
                "command": "python",
                "args": ["/path/to/sexual_health_bot/mcp_server.py"]
            }
        }
    }
"""

import asyncio
import os
import sys
import logging

# ── Fix: Ensure local 'agents' folder is prioritized over global site-packages ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP

# Import all agents
from agents.agent_general        import GeneralHealthAgent
from agents.agent_sti            import STIAgent
from agents.agent_contraception  import ContraceptionAgent
from agents.agent_reproductive   import ReproductiveHealthAgent
from agents.agent_safety         import SafetyConsentAgent
from agents.agent_coordinator    import CoordinatorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Create FastMCP server ─────────────────────────────────────────────────────
mcp = FastMCP(
    name="SexualHealthAssistant",
    instructions=(
        "A virtual assistant with 5 specialized agents for sexual health topics. "
        "Use the coordinator tool to auto-route, or call a specific agent directly."
    ),
)

# ── Instantiate agents once (shared state) ───────────────────────────────────
_general      = GeneralHealthAgent()
_sti          = STIAgent()
_contraception = ContraceptionAgent()
_reproductive = ReproductiveHealthAgent()
_safety       = SafetyConsentAgent()
_coordinator  = CoordinatorAgent()


# ════════════════════════════════════════════════════════════════════════════ #
#  MCP TOOLS                                                                   #
# ════════════════════════════════════════════════════════════════════════════ #

@mcp.tool()
def coordinator(question: str) -> str:
    """
    [RECOMMENDED] Auto-routes the question to the most relevant specialized agent.
    Use this when you are unsure which agent to call.

    Args:
        question: The user's sexual health question.

    Returns:
        The answer from the most suitable specialized agent,
        prefixed with which agent was used.
    """
    result = _coordinator.run(question)
    agent_used = result["agent_used"]
    answer     = result["answer"]
    return f"[Handled by: {agent_used}]\n\n{answer}"


@mcp.tool()
def general_health_agent(question: str) -> str:
    """
    Answers general sexual health questions: hygiene, anatomy, puberty,
    healthy sexuality, wellness, and when to see a doctor.

    Args:
        question: The user's general sexual health question.

    Returns:
        Educational answer about general sexual health.
    """
    return _general.run(question)


@mcp.tool()
def sti_agent(question: str) -> str:
    """
    Answers questions about sexually transmitted infections (STIs/STDs):
    HIV, chlamydia, gonorrhea, syphilis, herpes, HPV, hepatitis B/C.
    Covers symptoms, transmission, prevention, testing, and treatment.

    Args:
        question: The user's question about STIs or STDs.

    Returns:
        Educational information about sexually transmitted infections.
    """
    return _sti.run(question)


@mcp.tool()
def contraception_agent(question: str) -> str:
    """
    Answers questions about contraception (birth control) and family planning:
    condoms, pills, IUDs, implants, emergency contraception, fertility awareness.

    Args:
        question: The user's question about contraception or family planning.

    Returns:
        Information about contraceptive methods and family planning options.
    """
    return _contraception.run(question)


@mcp.tool()
def reproductive_health_agent(question: str) -> str:
    """
    Answers questions about reproductive health: menstruation, pregnancy,
    fertility, PCOS, endometriosis, menopause, and reproductive conditions.

    Args:
        question: The user's question about reproductive health.

    Returns:
        Information about reproductive biology and health conditions.
    """
    return _reproductive.run(question)


@mcp.tool()
def safety_consent_agent(question: str) -> str:
    """
    Answers questions about consent, healthy relationships, sexual violence,
    sexual coercion, and the emotional/psychological aspects of sexuality.
    Provides crisis resources when needed.

    Args:
        question: The user's question about consent, safety, or relationships.

    Returns:
        Supportive and educational information about sexual safety and consent.
    """
    return _safety.run(question)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting Sexual Health Assistant MCP Server …")
    logger.info("Available tools: coordinator, general_health_agent, sti_agent, "
                "contraception_agent, reproductive_health_agent, safety_consent_agent")
    mcp.run()