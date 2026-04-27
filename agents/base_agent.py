"""
base_agent.py
─────────────
Base class that every specialized agent inherits from.
It talks to the FPT Cloud (OpenAI-compatible) API.
"""

from openai import AsyncOpenAI
from config import API_URL, API_KEY, MODEL_NAME


class BaseAgent:
    """
    Base agent: wraps an OpenAI-compatible chat API call.
    Each subclass sets its own `name`, `description`, and `system_prompt`.
    """

    name: str = "base_agent"
    description: str = "A generic agent."
    system_prompt: str = "You are a helpful assistant."

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=API_URL,
            api_key=API_KEY if API_KEY else "no-key",
        )
        self.model = MODEL_NAME

    # ------------------------------------------------------------------ #
    #  Core run method                                                     #
    # ------------------------------------------------------------------ #
    async def run(self, question: str, chat_history: list[dict] | None = None) -> str:
        """
        Send a question to the LLM and return the text answer.
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if chat_history:
            messages.extend(chat_history)

        messages.append({"role": "user", "content": question})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    async def run_stream(self, question: str, chat_history: list[dict] | None = None):
        """
        Send a question to the LLM and yield tokens in real-time.
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if chat_history:
            messages.extend(chat_history)

        messages.append({"role": "user", "content": question})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True,  # Enable streaming
        )
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # ------------------------------------------------------------------ #
    #  MCP-style tool schema                                               #
    # ------------------------------------------------------------------ #
    def as_tool_schema(self) -> dict:
        """Return an OpenAI function-calling / MCP tool schema for this agent."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The user question to answer.",
                        }
                    },
                    "required": ["question"],
                },
            },
        }

    def __repr__(self):
        return f"<Agent name={self.name!r}>"