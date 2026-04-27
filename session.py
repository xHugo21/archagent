import subprocess
from dataclasses import dataclass
from typing import Callable

from ui import UserInterface
from utils import resolve_path


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

    def _get_agents_md(self) -> str | None:
        path = resolve_path(".AGENTS.md")
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception:
            return None

    def _initialize_messages(self) -> list[dict]:
        with open(resolve_path("prompts/master.txt"), "r") as f:
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

        return False

    def _handle_bang_command(self, user_input: str) -> bool:
        cmd = user_input.strip().lower()

        if cmd.startswith("!"):
            bash_command = user_input.strip()[1:].strip()
            try:
                result = subprocess.run(
                    bash_command, shell=True, capture_output=True, text=True
                )
                self.ui.display_bang_message(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
            except Exception as e:
                print(f"An error occurred: {e}")
            return True

        return False
