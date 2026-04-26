from ui import UserInterface, Message
from typing import Callable


class Session:
    def __init__(self, messages: list[dict]):
        self.ui = UserInterface()
        self.agent_callback = None
        self.messages: list[dict] = messages

    def run(
        self, agent_callback: Callable[[str, list[dict]], tuple[str, list[dict]]]
    ) -> None:
        self.agent_callback = agent_callback
        self.ui.display_welcome()
        self.ui.display_help()

        while self.ui.running:
            try:
                user_input = self.ui.get_user_input()

                if self._handle_slash_command(user_input):
                    continue

                user_msg = Message(role="user", content=user_input)
                self.ui.display_message(user_msg)
                self.messages.append({"role": "user", "content": user_input})

                self.ui.display_processing()
                response, self.messages = self.agent_callback(user_input, self.messages)
                self.ui.stop_processing()

                agent_msg = Message(role="assistant", content=response)
                self.ui.display_message(agent_msg)

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
