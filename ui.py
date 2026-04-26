from rich.text import Text
from rich.console import Console
from rich.status import Status
from rich.align import Align
from rich.rule import Rule


class UserInterface:
    def __init__(self):
        self.console = Console()
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

    def display_rule(self) -> None:
        self.console.print(Rule())

    def display_agent_message(self, content: str) -> None:
        self.console.print(Text(f"{content}", style="bold green"))
        self.display_rule()

    def display_error(self, error: str) -> None:
        self.console.print(Text(f"Error: {error}", style="bold red"))
        self.display_rule()

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
