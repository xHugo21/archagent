from dataclasses import dataclass
from rich.text import Text
from rich.console import Console
from rich.status import Status
from rich.align import Align


@dataclass
class Message:
    role: str
    content: str
    tool_call_id: str | None = None
    function_name: str | None = None


class UserInterface:
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

        self.console.print(Align.center(logo))

    def display_message(self, message: Message) -> None:
        self.messages.append(message)

        if message.role == "user":
            self.console.print(Text(f"{message.content}", style="white"))
        elif message.role == "assistant":
            self.console.print(Text(f"{message.content}", style="bold green"))

    def display_error(self, error: str) -> None:
        self.console.print(Text(f"❌ Error: {error}", style="bold red"))

    def display_tool_execution(self, tool_name: str) -> None:
        self.console.print(
            Text(
                f"Running {tool_name}",
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
        """
        self.console.print(help_text)
