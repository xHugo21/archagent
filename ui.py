import json
import os

from rich.text import Text
from rich.console import Console, Group
from rich.status import Status
from rich.align import Align
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.padding import Padding

ACCENT = "cyan"
TOOL_COLOR = "magenta"
INFO_COLOR = "grey53"


class UserInterface:
    def __init__(self):
        self.console = Console(highlight=False)
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
                    logo.stylize(
                        "bold cyan", line_start + col_start, line_start + col_end
                    )
                    break
            line_start += len(merged_line) + 1

        self.console.print(Align.center(logo))

    def display_rule(self, color: str = "white") -> None:
        self.console.print(Rule(style=color))

    def _render_output(self, output: str | None):
        if output is None:
            return Text("(no output)", style=INFO_COLOR)
        if not output.strip():
            return Text("(empty output)", style=INFO_COLOR)

        stripped = output.strip()
        if stripped[:1] in "{[":
            try:
                parsed = json.loads(stripped)
            except (ValueError, TypeError):
                parsed = None
            if parsed is not None:
                pretty = json.dumps(parsed, indent=2, ensure_ascii=False)
                return Syntax(
                    pretty, "json", background_color="default", word_wrap=True
                )

        return Text(output.rstrip("\n"), overflow="fold")

    def display_agent_message(self, content: str) -> None:
        content = (content or "").strip()
        if not content:
            return
        self.console.print(Rule(Text("archagent", style=f"bold {ACCENT}"), style=ACCENT))
        self.console.print(Markdown(content))
        self.console.print()

    def display_info_message(self, content: str) -> None:
        self.console.print(
            Padding(
                Text.assemble(
                    ("• ", INFO_COLOR), (content, INFO_COLOR), overflow="fold"
                ),
                (0, 0, 0, 2),
            )
        )

    def display_error(self, content: str) -> None:
        self.console.print(
            Panel(
                Text(content, style="red", overflow="fold"),
                title=Text("Error", style="bold red"),
                title_align="left",
                border_style="red",
                box=ROUNDED,
                padding=(0, 1),
            )
        )

    def display_tool_execution(
        self,
        tool_name: str,
        output: str | None = None,
        duration: float | None = None,
    ) -> None:
        title = Text.assemble(("Ran ", TOOL_COLOR), (tool_name, f"bold {TOOL_COLOR}"))
        if duration is not None:
            title.append(f"  {duration:.3f}s", style=INFO_COLOR)

        self.console.print(
            Panel(
                self._render_output(output),
                title=title,
                title_align="left",
                border_style=TOOL_COLOR,
                box=ROUNDED,
                padding=(0, 1),
            )
        )

    def confirm_tool_execution(
        self,
        tool_name: str,
        args: dict,
        reason: str,
        mode: str,
    ) -> str:
        body = Group(
            Text.assemble(("mode: ", INFO_COLOR), (mode, "yellow"), overflow="fold"),
            Text.assemble(
                ("reason: ", INFO_COLOR), (reason, "yellow"), overflow="fold"
            ),
            Text("arguments:", style=INFO_COLOR),
            Syntax(
                json.dumps(args, indent=2, ensure_ascii=False),
                "json",
                background_color="default",
                word_wrap=True,
            ),
        )
        self.console.print(
            Panel(
                body,
                title=Text(f"Approval needed: {tool_name}", style="bold yellow"),
                title_align="left",
                border_style="yellow",
                box=ROUNDED,
                padding=(0, 1),
            )
        )

        answer = (
            self.console.input(
                Text(
                    "Allow? [y/N] (a = yes + stop asking this session): ",
                    style="bold yellow",
                )
            )
            .strip()
            .lower()
        )

        if answer in {"a", "auto"}:
            return "auto"

        return "yes" if answer in {"y", "yes"} else "no"

    def get_user_input(self, prompt: str = "❯ ") -> str:
        return self.console.input(Text(prompt, style=f"bold {ACCENT}"))

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
        text = Text()
        text.append(" /exit", style=f"bold {ACCENT}")
        text.append(" quit    ", style=INFO_COLOR)
        text.append("/clear", style=f"bold {ACCENT}")
        text.append(" reset    ", style=INFO_COLOR)
        text.append("/help", style=f"bold {ACCENT}")
        text.append(" commands    ", style=INFO_COLOR)
        text.append("/mode", style=f"bold {ACCENT}")
        text.append(" permissions    ", style=INFO_COLOR)
        text.append("/auto", style=f"bold {ACCENT}")
        text.append(" approvals", style=INFO_COLOR)
        self.console.print(Align.center(text))

    def display_footer(
        self,
        used_tokens: int,
        context_window: int | None,
        cwd: str,
        model: str,
        auto_approve: bool = False,
    ) -> None:
        used_text = str(used_tokens)
        context_text = "-" if context_window is None else str(context_window)

        percent_text = "-"
        if context_window is not None and context_window > 0:
            percent_text = f"{(used_tokens / context_window) * 100:.1f}%"

        home = os.path.expanduser("~")
        cwd_text = cwd.replace(home, "~", 1) if home and cwd.startswith(home) else cwd
        model_text = model or "-"
        tokens_text = f"tokens: {used_text}/{context_text} ({percent_text})"

        self.console.print(Rule(style="grey30"))

        if self.console.width < 100:
            line = Text(overflow="fold")
            line.append(cwd_text, style=INFO_COLOR)
            line.append("  ·  ", style="grey30")
            line.append(tokens_text, style=INFO_COLOR)
            line.append("  ·  ", style="grey30")
            if auto_approve:
                line.append("auto-approve", style="yellow")
                line.append(" · ", style="grey30")
            line.append(model_text, style=INFO_COLOR)
            self.console.print(line)
            return

        auto_text = "[yellow]auto-approve[/yellow] · " if auto_approve else ""

        footer = Table.grid(expand=True)
        footer.add_column(justify="left", no_wrap=True, overflow="ellipsis")
        footer.add_column(justify="center", no_wrap=True, overflow="ellipsis")
        footer.add_column(justify="right", no_wrap=True, overflow="ellipsis")
        footer.add_row(
            f"[grey53]{cwd_text}[/grey53]",
            f"[grey53]{tokens_text}[/grey53]",
            f"{auto_text}[grey53]{model_text}[/grey53]",
        )
        self.console.print(footer)
