from typing import Any, cast
from session import Session
import json
from tools import tools, run_bash_command
import litellm


class Agent:
    def __init__(self, model: str, api_key: str, session: Session):
        self.model = model
        self.api_key = api_key
        self.session = session

    def run(self, user_prompt: str, messages: list[Any]) -> tuple[str, list[Any]]:
        messages_copy = messages.copy()
        messages_copy.append({"role": "user", "content": user_prompt})

        while True:
            response = litellm.completion(
                model=self.model,
                api_key=self.api_key,
                messages=messages_copy,
                stream=False,
                tools=tools,
            )

            response = cast(litellm.ModelResponse, response)

            message_obj = response.choices[0].message
            message_dict: dict[str, Any] = {
                "role": "assistant",
                "content": message_obj.content or "",
            }
            if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
                message_dict["tool_calls"] = message_obj.tool_calls

            messages_copy.append(message_dict)

            if not message_obj.tool_calls:
                return message_obj.content or "", messages_copy

            for tool_call in message_obj.tool_calls:
                self._execute_tool(tool_call, messages_copy)

    def _execute_tool(self, tool_call: Any, messages_copy: list[Any]) -> None:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        self.session.ui.display_tool_execution(function_name)

        if function_name == "run_bash_command":
            result = run_bash_command(args["command"])
        else:
            result = "Error: Tool not found"

        messages_copy.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result,
            }
        )
