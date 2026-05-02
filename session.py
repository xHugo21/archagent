import os
import subprocess
from dataclasses import dataclass
from typing import Callable

from ui import UserInterface
from utils import resolve_workspace_path, resolve_user_path


@dataclass
class Message:
    role: str
    content: str
    tool_call_id: str | None = None
    function_name: str | None = None


class Session:
    def __init__(self):
        self.ui = UserInterface()
        self.agent_callback = None
        self.messages: list[dict] = self._initialize_messages()
        self.used_tokens: int = 0
        self.context_window: int | None = None
        self.model: str = ""
        self.permission_mode: str = "normal"

    def _get_agents_md(self) -> str | None:
        workspace_path = resolve_workspace_path("AGENTS.md")
        user_path = resolve_user_path("~/.agents/AGENTS.md")

        for path in (workspace_path, user_path):
            try:
                with open(path, "r") as f:
                    return f.read()
            except FileNotFoundError:
                continue
            except Exception:
                continue

    def _initialize_messages(self) -> list[dict]:
        with open(resolve_workspace_path("master.txt"), "r") as f:
            system_prompt = f.read()

        agents_md = self._get_agents_md()
        if agents_md is not None:
            system_prompt = f"{system_prompt.rstrip()}\n\n{agents_md.strip()}"

        return [{"role": "system", "content": system_prompt}]

    def run(
        self, agent_callback: Callable[[str, list[dict]], tuple[str, list[dict]]]
    ) -> None:
        self.agent_callback = agent_callback
        self.ui.clear_screen()

        while self.ui.running:
            try:
                user_input = self.ui.get_user_input()

                if self._handle_slash_command(user_input):
                    continue

                elif self._handle_bang_command(user_input):
                    continue

                self.messages.append({"role": "user", "content": user_input})

                self.ui.display_processing()
                response, self.messages = self.agent_callback(user_input, self.messages)
                self.ui.stop_processing()

                self.ui.display_agent_message(response)
                self.ui.display_footer(
                    self.used_tokens,
                    self.context_window,
                    os.getcwd(),
                    self.model,
                )
                self.messages.append({"role": "assistant", "content": response})

            except KeyboardInterrupt:
                self.ui.running = False
            except Exception as e:
                self.ui.display_error(str(e))

    def _handle_slash_command(self, user_input: str) -> bool:
        cmd = user_input.strip().lower()

        if cmd == "/exit":
            self.ui.running = False
            return True

        if cmd == "/clear":
            self.ui.clear_screen()
            return True

        if cmd == "/help":
            self.ui.display_help()
            return True

        if cmd.startswith("/mode"):
            parts = user_input.strip().split()
            if len(parts) == 1:
                self.ui.display_info_message(
                    f"Permission mode: {self.permission_mode} (safe | normal | full)"
                )
                return True

            next_mode = parts[1].strip().lower()
            if next_mode not in {"safe", "normal", "full"}:
                self.ui.display_error("Invalid mode. Use: /mode safe | normal | full")
                return True

            self.permission_mode = next_mode
            self.ui.display_info_message(
                f"Permission mode set to: {self.permission_mode}"
            )
            return True

        return False

    def _handle_bang_command(self, user_input: str) -> bool:
        cmd = user_input.strip().lower()

        if cmd.startswith("!"):
            bash_command = user_input.strip()[1:].strip()
            try:
                result = subprocess.run(
                    bash_command, shell=True, capture_output=True, text=True
                )
                self.ui.display_info_message(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
            except Exception as e:
                print(f"An error occurred: {e}")
            return True

        return False
