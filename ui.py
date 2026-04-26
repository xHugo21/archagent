from typing import Callable
from dataclasses import dataclass
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich import box
import json


@dataclass
class Message:
    role: str
    content: str
    tool_call_id: str | None = None
    function_name: str | None = None


class ChatApp:
    def __init__(self):
        self.console = Console()
        self.messages: list[Message] = []
        self.running = True
        self.loading = Status(
            "[cyan] Processing...", console=self.console, spinner="dots"
        )

    def display_welcome(self) -> None:
        logo = Text(
            "\n".join(
                [
                    "    _             _        _                    _   ",
                    "   / \\   _ __ ___| |__    / \\   __ _  ___ _ __ | |_ ",
                    "  / _ \\ | '__/ __| '_ \\  / _ \\ / _` |/ _ \\ '_ \\| __|",
                    " / ___ \\| | | (__| | | |/ ___ \\ (_| |  __/ | | | |_ ",
                    "/_/   \\_\\_|  \\___|_| |_/_/   \\_\\__, |\\___|_| |_|\\__|",
                    "                               |___/               ",
                ]
            ),
            style="bold cyan",
        )

        welcome = Panel(
            logo,
            border_style="bright_cyan",
            box=box.ROUNDED,
            padding=(1, 2),
            title_align="center",
        )
        self.console.print(welcome)

    def display_message(self, message: Message) -> None:
        self.messages.append(message)

        if message.role == "user":
            self.console.print(Text(f"You: {message.content}", style="cyan"))
        elif message.role == "assistant":
            self.console.print(Text(f"Agent: {message.content}", style="bold green"))
        elif message.role == "tool":
            self.console.print(
                Text(
                    f"🔧 Tool [{message.function_name}]: {message.content}",
                    style="yellow",
                )
            )

    def display_error(self, error: str) -> None:
        self.console.print(Text(f"❌ Error: {error}", style="bold red"))

    def display_tool_execution(self, tool_name: str, args: dict) -> None:
        self.console.print(
            Text(
                f"🔧 Running Tool: {tool_name} with {json.dumps(args)}",
                style="yellow",
            )
        )

    def get_user_input(self, prompt: str = "> ") -> str:
        return self.console.input(Text(prompt, style="bold cyan"))

    def display_processing(self) -> None:
        self.loading.start()

    def stop_processing(self) -> None:
        if self.loading:
            self.loading.stop()

    def clear_screen(self) -> None:
        self.console.clear()

    def display_help(self) -> None:
        help_text = """
[yellow]Slash Commands:[/yellow]
  /exit     - Exit the application
  /clear    - Clear the screen
  /help     - Show this help message

[yellow]Usage:[/yellow]
  Just type your question or command and press Enter.
  The agent will process your request and show the results.
        """
        self.console.print(help_text)


class InteractiveSession:
    def __init__(self, messages: list[dict]):
        self.app = ChatApp()
        self.agent_callback = None
        self.messages: list[dict] = messages

    def run(
        self, agent_callback: Callable[[str, list[dict]], tuple[str, list[dict]]]
    ) -> None:
        self.agent_callback = agent_callback
        self.app.display_welcome()
        self.app.display_help()

        while self.app.running:
            try:
                user_input = self.app.get_user_input()

                if self._handle_slash_command(user_input):
                    continue

                user_msg = Message(role="user", content=user_input)
                self.app.display_message(user_msg)
                self.messages.append({"role": "user", "content": user_input})

                self.app.display_processing()
                response, self.messages = self.agent_callback(user_input, self.messages)
                self.app.stop_processing()

                agent_msg = Message(role="assistant", content=response)
                self.app.display_message(agent_msg)

            except KeyboardInterrupt:
                self.app.console.print(Text("\nGoodbye!", style="bold yellow"))
                self.app.running = False
            except Exception as e:
                self.app.display_error(str(e))

    def _handle_slash_command(self, user_input: str) -> bool:
        cmd = user_input.strip().lower()

        if cmd == "/exit":
            self.app.running = False
            return True

        if cmd == "/clear":
            self.app.clear_screen()
            return True

        if cmd == "/help":
            self.app.display_help()
            return True

        return False
