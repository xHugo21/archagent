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
        archagent = [
            "    _             _        _                    _   ",
            "   / \\   _ __ ___| |__    / \\   __ _  ___ _ __ | |_ ",
            "  / _ \\ | '__/ __| '_ \\  / _ \\ / _` |/ _ \\ '_ \\| __|",
            " / ___ \\| | | (__| | | |/ ___ \\ (_| |  __/ | | | |_ ",
            "/_/   \\_\\_|  \\___|_| |_/_/   \\_\\__, |\\___|_| |_|\\__|",
            "                               |___/               ",
        ]

        wings = [
            "⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⣼⠟⢡⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠙⢿⡄⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⣴⡏⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠈⣿⡄⠀⠀⠀⠀",
            "⠀⠀⠀⢀⣴⡏⠃⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠁⣿⣄⠀⠀⠀",
            "⠀⠀⢀⡾⠁⣇⠀⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⠀⢠⡇⠹⣆⠀⠀",
            "⠀⠀⢸⡁⠀⣿⠑⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⢩⡇⠀⢹⠀⠀",
            "⠀⠀⢸⣧⡀⣿⣆⠀⠀⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠃⠀⢀⣼⠇⢠⣾⠀⠀",
            "⠀⢠⠾⡇⠁⠘⣿⡉⠀⠀⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠁⠀⠀⣹⡿⠀⠀⡿⢦⠀",
            "⠀⡿⠀⢿⣆⠀⠱⣿⡆⠀⠀⠘⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠀⠀⠀⣾⣿⠁⢀⣼⠃⠘⡆",
            "⠀⣿⡀⢈⢷⡀⠀⠱⡿⣦⣀⡀⢰⡹⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⢣⠀⢀⣠⣾⡿⠁⠀⣠⠏⠀⢰⡇",
            "⣴⢿⡄⠈⢯⢿⡖⠀⣿⢿⢷⣍⣈⣷⡈⠙⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠞⠋⣰⡟⢀⣹⢿⣿⡇⠐⣺⣯⠇⠀⣸⢧",
            "⣏⠈⢷⣄⠀⠳⣿⣦⣌⣻⣿⡏⠙⠻⣟⠀⠀⠈⠓⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠖⠋⠁⠀⢸⡿⠛⠉⢿⡿⢋⣠⣾⡿⠋⢀⣴⠏⠈",
            "⠹⡄⠈⣿⣅⠀⠘⣿⣷⣍⢻⣇⣷⠄⠈⠳⣤⡀⠀⠀⠈⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠶⠋⠀⠀⠀⣀⣴⠋⠀⢠⡇⣾⢋⣤⣿⡿⠁⢀⣽⠋⠀⡴",
            "⠀⢻⠦⠹⣝⣷⡂⠈⣿⣿⠛⠻⣮⡃⠀⠀⣿⣿⡶⣄⣀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠞⠁⠀⢀⣀⡴⣾⣽⡿⠀⠀⣾⡿⠛⠻⣿⡟⠀⣲⣿⡽⠡⢾⠃",
            "⠀⠈⣷⣄⠈⠳⣝⣧⡀⢿⣷⣀⠈⠙⠶⣄⡚⠽⣿⣿⡉⠙⠂⠀⠀⠹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠁⠀⠀⠘⠋⣝⣿⣻⠕⣂⣴⠞⠉⠀⣠⣿⠇⣠⢾⡿⠋⢀⣰⡏⠀",
            "⠀⠀⢸⠙⢯⣅⠀⢽⡯⣿⢷⣽⣂⠀⠀⣓⡯⣗⣾⣷⣄⡀⠀⠀⠀⠀⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⣀⣽⣿⣖⡿⣟⡋⠀⢀⣺⣷⢿⣻⣿⠉⢀⣩⠟⢹⠃⠀",
            "⠀⠀⠈⢧⡀⠙⣿⣇⣉⠻⣿⡋⠉⠓⠶⡤⢭⣽⣿⡅⠀⠀⠀⠀⣴⠞⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⣄⠀⠀⠀⠀⣽⣿⣭⠥⠴⠖⠋⠉⣻⡿⢋⣁⣽⡟⠁⣠⠟⠀⠀",
            "⠀⠀⠀⠘⣿⡂⠈⠓⢯⣷⣿⣿⣾⠤⠀⠩⠭⢽⣿⣦⡴⠀⠀⠀⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡇⠀⠀⠰⣦⣾⣿⠭⠭⠁⢀⣬⣾⣿⣷⣿⠟⠋⠀⣺⡿⠀⠀⠀",
            "⠀⠀⠀⠀⠈⠛⢶⣤⠀⠈⠻⣿⣿⣿⠶⠶⠶⣒⣿⣿⡶⠀⡀⠀⠈⠙⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠞⠉⠀⠀⣄⠠⣼⣿⣖⡒⠲⠶⢾⣿⣿⡿⠉⠀⢠⣴⠾⠋⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠈⠉⠓⠒⣼⣟⡁⠀⠀⢀⣀⡭⣟⣿⣾⠁⠀⡀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⣀⢀⢹⣿⣿⣿⣅⣀⠀⠀⠀⠘⣿⡔⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣃⣴⠞⠋⠁⠈⣛⣽⣿⣶⣾⠃⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⡼⠋⠀⢀⢀⢹⣾⣿⣿⢯⡋⠁⠉⠙⢶⣄⣻⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⣶⡀⢠⠞⠁⠉⣵⣿⣿⣦⣼⡀⠀⠀⠙⢦⡀⠀⠀⣠⠞⠁⠀⠀⣸⣾⣾⢿⢷⣍⠀⠙⢦⣀⣰⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠻⢶⡏⠀⠀⡼⠁⢉⡿⠋⡽⠉⠉⠉⠓⠚⠉⠀⠀⠙⠒⠋⠉⠉⠹⡍⠿⣇⠁⠹⡆⠀⣈⢿⠾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠭⠿⣧⣖⣼⡧⢦⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠢⢻⣔⣲⡿⢿⡽⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        ]

        merged_logo = wings[:]
        start = max((len(wings) - len(archagent)) // 2, 0)
        for i, line in enumerate(archagent):
            wing_line = merged_logo[start + i]
            mid = len(wing_line) // 2
            half = len(line) // 2
            merged_logo[start + i] = (
                wing_line[: mid - half] + line + wing_line[mid + (len(line) - half) :]
            )

        logo = Text("\n".join(merged_logo + ["\n"]), style="bold cyan")
        self.console.print(Align.center(logo))

    def display_rule(self, color: str = "white") -> None:
        self.console.print(Rule(style=color))

    def _display_message(self, content: str, color: str) -> None:
        self.display_rule(color)
        self.console.print(Text(content, style=color))
        self.display_rule(color)

    def display_agent_message(self, content: str) -> None:
        self._display_message(content, "cyan")

    def display_tool_execution(self, tool_name: str, output: str | None = None) -> None:
        content = f"Ran {tool_name}\n"
        if output is not None:
            content += f"\nOutput:\n{output}"
        self._display_message(content, "magenta")

    def display_error(self, content: str) -> None:
        self._display_message(content, "red")

    def get_user_input(self, prompt: str = "> ") -> str:
        return self.console.input(Text(prompt, style="bold cyan"))

    def display_processing(self) -> None:
        self.loading.start()

    def stop_processing(self) -> None:
        if self.loading:
            self.loading.stop()

    def clear_screen(self) -> None:
        self.console.clear()
        self.display_welcome()

    def display_help(self) -> None:
        help_text = """/exit | /clear | /help"""
        self.console.print(Align.center(help_text))
