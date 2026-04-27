import json
import os
from typing import Any, cast

from dotenv import load_dotenv
import litellm

from session import Session
import tools as tool_impl


class Agent:
    def __init__(self, session: Session):
        self.model, self.api_key = self._get_env_vars()
        self.session = session

    def _get_env_vars(self) -> tuple[str, str]:
        load_dotenv()

        model = os.environ["LITELLM_MODEL"] or ""
        api_key = os.environ["LITELLM_API_KEY"] or ""

        return model, api_key

    def run(self, user_prompt: str, messages: list[Any]) -> tuple[str, list[Any]]:
        messages_copy = messages.copy()
        messages_copy.append({"role": "user", "content": user_prompt})

        while True:
            response = litellm.completion(
                model=self.model,
                api_key=self.api_key,
                messages=messages_copy,
                stream=False,
                tools=tool_impl.tools,
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

        handler = getattr(tool_impl, function_name, None)

        if not callable(handler):
            result: str = "Error: Tool not found"
        else:
            try:
                raw_result = handler(**args)
                result = (
                    raw_result
                    if isinstance(raw_result, str)
                    else json.dumps(raw_result)
                )
            except TypeError as e:
                result = f"Execution Error: Invalid tool arguments - {str(e)}"
            except Exception as e:
                result = f"Execution Error: {str(e)}"

        self.session.ui.display_tool_execution(function_name, result)

        messages_copy.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result,
            }
        )
