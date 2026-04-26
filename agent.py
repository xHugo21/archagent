from typing import Any, cast
from session import Session
import json
from tools import (
    apply_patch,
    delete_file,
    edit_file,
    find_files,
    list_files,
    move_file,
    read_file,
    search_text,
    tools,
    write_file,
)
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

        tool_map = {
            "read_file": lambda a: read_file(
                a["path"], a.get("start_line", 1), a.get("end_line")
            ),
            "edit_file": lambda a: edit_file(a["path"], a["old_text"], a["new_text"]),
            "write_file": lambda a: write_file(a["path"], a["content"]),
            "list_files": lambda a: list_files(a.get("path", "."), a.get("recursive", False)),
            "search_text": lambda a: search_text(a["query"], a.get("path", ".")),
            "find_files": lambda a: find_files(a["pattern"], a.get("path", ".")),
            "move_file": lambda a: move_file(a["source_path"], a["destination_path"]),
            "delete_file": lambda a: delete_file(a["path"], a.get("recursive", False)),
            "apply_patch": lambda a: apply_patch(a["path"], a["old_text"], a["new_text"]),
        }

        handler = tool_map.get(function_name)
        if handler is None:
            result = "Error: Tool not found"
        else:
            try:
                result = handler(args)
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
