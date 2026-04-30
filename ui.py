from rich.text import Text
from rich.console import Console
from rich.status import Status
from rich.align import Align
from rich.rule import Rule
from rich.table import Table


class UserInterface:
    def __init__(self):
        self.console = Console()
        self.running = True
        self.loading = Status(
            "[grey53]Processing...", console=self.console, spinner="dots"
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
        arch_spans: list[tuple[int, int, int]] = []

        for i, line in enumerate(archagent):
            wing_line = merged_logo[start + i]
            mid = len(wing_line) // 2
            half = len(line) // 2
            insert_start = mid - half
            insert_end = insert_start + len(line)
            merged_logo[start + i] = (
                wing_line[:insert_start] + line + wing_line[insert_end:]
            )
            arch_spans.append((start + i, insert_start, insert_end))

        logo_content = "\n".join(merged_logo) + "\n"
        logo = Text(logo_content, style="bold white")

        line_start = 0
        for line_index, merged_line in enumerate(merged_logo):
            for span_line, col_start, col_end in arch_spans:
                if span_line == line_index:
                    logo.stylize("bold cyan", line_start + col_start, line_start + col_end)
                    break
            line_start += len(merged_line) + 1

        self.console.print(Align.center(logo))

    def display_rule(self, color: str = "white") -> None:
        self.console.print(Rule(style=color))

    def _display_message(self, content: str, color: str) -> None:
        self.display_rule(color)
        self.console.print(Text(content, style=color))
        self.display_rule(color)

    def display_agent_message(self, content: str) -> None:
        self._display_message(content, "cyan")

    def display_bang_message(self, content: str) -> None:
        self._display_message(content, "grey53")

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
        self.display_help()

    def display_help(self) -> None:
        help_text = """/exit | /clear | /help"""
        self.console.print(Align.center(help_text))

    def display_footer(
        self,
        used_tokens: int,
        context_window: int | None,
        cwd: str,
        model: str,
    ) -> None:
        used_text = str(used_tokens)
        context_text = "-" if context_window is None else str(context_window)

        percent_text = "-"
        if context_window is not None and context_window > 0:
            percent_text = f"{(used_tokens / context_window) * 100:.1f}%"

        model_text = model or "-"

        footer = Table.grid(expand=True)
        footer.add_column(justify="left")
        footer.add_column(justify="center")
        footer.add_column(justify="right")
        footer.add_row(
            f"[grey53]{cwd}[/grey53]",
            f"[grey53]tokens: {used_text}/{context_text} ({percent_text})[/grey53]",
            f"[grey53]{model_text}[/grey53]",
        )
        self.console.print(footer)
