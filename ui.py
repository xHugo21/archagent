from typing import Callable
from dataclasses import dataclass
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Input, Static, RichLog, Button
from rich.text import Text
from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.align import Align
import json


@dataclass
class Message:
    role: str
    content: str
    tool_call_id: str | None = None
    function_name: str | None = None


class ChatDisplay(RichLog):
    def add_message(self, message: Message) -> None:
        if message.role == "user":
            self.write(Text("You: ", style="bold cyan"))
            self.write(Text(message.content, style="cyan"))
        elif message.role == "assistant":
            self.write(Text("Agent: ", style="bold green"))
            self.write(Text(message.content, style="green"))
        elif message.role == "tool":
            self.write(
                Text(f"🔧 Tool [{message.function_name}]: ", style="bold yellow"),
            )
            self.write(Text(message.content, style="yellow"))


class ChatInput(Container):
    DEFAULT_CSS = """
    ChatInput {
        height: 3;
        layout: horizontal;
    }

    ChatInput Input {
        width: 1fr;
    }

    ChatInput Button {
        width: 10;
    }
    """

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type your message...", id="message_input")
        yield Button("Send", id="send_btn", variant="primary")

    def get_input_text(self) -> str:
        input_widget = self.query_one("#message_input", Input)
        return input_widget.value

    def clear_input(self) -> None:
        input_widget = self.query_one("#message_input", Input)
        input_widget.value = ""


class StatusBar(Static):
    def render(self) -> RenderableType:
        status_text = getattr(self, "status_text", "Ready")
        return Align.left(Text(status_text, style="bold white on blue"))

    def set_status(self, text: str) -> None:
        self.status_text = text
        self.refresh()


class ChatApp:
    def __init__(self):
        self.console = Console()
        self.messages: list[Message] = []
        self.running = True

    def display_welcome(self) -> None:
        welcome = Panel(
            Text.assemble(
                "Welcome to ",
                Text("ArchAgent", style="bold cyan"),
                "\n\nYour AI terminal assistant",
            ),
            border_style="cyan",
            padding=(1, 2),
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
        self.console.print(Text("⏳ Processing your request...", style="dim yellow"))

    def clear_screen(self) -> None:
        self.console.clear()

    def display_help(self) -> None:
        help_text = """
[bold cyan]ArchAgent Help[/bold cyan]

[yellow]Commands:[/yellow]
  exit, quit, q     - Exit the application
  clear, cls        - Clear the screen
  help              - Show this help message

[yellow]Usage:[/yellow]
  Just type your question or command and press Enter.
  The agent will process your request and show the results.
        """
        self.console.print(help_text)


class InteractiveSession:
    def __init__(
        self,
        agent_loop_callback: Callable[[str, list[dict]], tuple[str, list[dict]]],
        messages: list[dict],
    ):
        self.app = ChatApp()
        self.agent_callback = agent_loop_callback
        self.messages: list[dict] = messages

    def run(self) -> None:
        self.app.display_welcome()
        self.app.display_help()

        while self.app.running:
            try:
                user_input = self.app.get_user_input()

                if self._handle_command(user_input):
                    continue

                user_msg = Message(role="user", content=user_input)
                self.app.display_message(user_msg)
                self.messages.append({"role": "user", "content": user_input})

                self.app.display_processing()
                response, self.messages = self.agent_callback(user_input, self.messages)

                agent_msg = Message(role="assistant", content=response)
                self.app.display_message(agent_msg)

            except KeyboardInterrupt:
                self.app.console.print(Text("\nGoodbye!", style="bold yellow"))
                self.app.running = False
            except Exception as e:
                self.app.display_error(str(e))

    def _handle_command(self, user_input: str) -> bool:
        cmd = user_input.strip().lower()

        if cmd in ("exit", "quit", "q"):
            self.app.console.print(Text("Goodbye!", style="bold yellow"))
            self.app.running = False
            return True

        if cmd in ("clear", "cls"):
            self.app.clear_screen()
            return True

        if cmd == "help":
            self.app.display_help()
            return True

        return False
