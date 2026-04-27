"""
chatbot.py (WebSocket Streaming Client)
────────────────────────────────────────
A standalone CLI client that uses WebSockets for real-time streaming.
"""

import sys
import asyncio
import json
import websockets
from rich.console import Console
from rich.panel   import Panel
from rich.live    import Live
from rich.markdown import Markdown

# ── Configuration ──
WS_URL = "ws://localhost:8010/ws/chat"
console = Console()

def print_banner():
    console.print(Panel.fit(
        "[bold cyan]🏥 Sexual Health Assistant (Streaming Mode)[/bold cyan]\n"
        "[dim]Connected via WebSocket to port 9010[/dim]",
        border_style="cyan",
    ))
    console.print("[dim]Type your question. Type /exit to quit, /clear to reset history.[/dim]\n")

async def chat_client():
    chat_history = []
    print_banner()

    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                try:
                    user_input = await asyncio.to_thread(console.input, "[bold yellow]You:[/bold yellow] ")
                    user_input = user_input.strip()
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[yellow]Goodbye![/yellow]")
                    break

                if not user_input:
                    continue

                if user_input.lower() in ("/exit", "/quit"):
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                
                if user_input.lower() == "/clear":
                    chat_history = []
                    console.print("[yellow]History cleared.[/yellow]")
                    continue

                # ── Send to WebSocket ──
                payload = {"message": user_input, "history": chat_history}
                await ws.send(json.dumps(payload))

                # ── Receive Streaming Response ──
                agent_used = "..."
                full_answer = ""
                
                # First message usually contains info about the agent
                msg = await ws.recv()
                data = json.loads(msg)
                if data["type"] == "info":
                    agent_used = data.get("message", "unknown")
                    console.print(f"\n[bold blue]→ {agent_used}[/bold blue]\n")

                # Setup Live display for streaming
                with Live(console=console, refresh_per_second=10) as live:
                    async for msg in ws:
                        data = json.loads(msg)
                        
                        if data["type"] == "token":
                            full_answer += data["content"]
                            live.update(Panel(
                                Markdown(full_answer),
                                title=f"[bold green]Assistant[/bold green]",
                                border_style="green",
                            ))
                        
                        elif data["type"] == "done":
                            # Final state
                            full_answer = data["content"]
                            live.update(Panel(
                                Markdown(full_answer),
                                title=f"[bold green]Assistant[/bold green]",
                                border_style="green",
                            ))
                            break
                        
                        elif data["type"] == "error":
                            console.print(f"[red]Error: {data['detail']}[/red]")
                            break

                # Update history
                chat_history.append({"role": "user", "content": user_input})
                chat_history.append({"role": "assistant", "content": full_answer})

                if len(chat_history) > 20:
                    chat_history = chat_history[-20:]

    except ConnectionRefusedError:
        console.print(f"[bold red]Error: Could not connect to WebSocket at {WS_URL}.[/bold red]")
        console.print("[dim]Make sure 'main.py' is running.[/dim]\n")
    except Exception as e:
        console.print(f"[red]Connection error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(chat_client())