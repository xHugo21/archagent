import os
from typing import Any, cast
from dotenv import load_dotenv
from ui import InteractiveSession
import json
import litellm
from tools import tools, run_bash_command

litellm.suppress_debug_info = True


def get_env_vars():
    load_dotenv()

    model = os.environ["LITELLM_MODEL"] or ""
    api_key = os.environ["LITELLM_API_KEY"] or ""

    return model, api_key


def initialize_messages():
    with open("prompts/master.txt", "r") as f:
        system_prompt = f.read()

    messages = [{"role": "system", "content": system_prompt}]

    return messages


def agent_loop(
    user_prompt: str,
    messages: list[Any],
    model: str,
    api_key: str,
) -> tuple[str, list[Any]]:

    messages_copy = messages.copy()
    messages_copy.append({"role": "user", "content": user_prompt})

    while True:
        response = litellm.completion(
            model=model,
            api_key=api_key,
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
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

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


def main():
    model, api_key = get_env_vars()
    messages = initialize_messages()

    session = InteractiveSession(
        lambda user_input, messages: agent_loop(user_input, messages, model, api_key),
        messages,
    )
    session.run()


if __name__ == "__main__":
    main()
