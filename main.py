def main():
    from sys import argv
    import os
    import json
    from dotenv import load_dotenv
    from typing import Any, cast
    import litellm
    from tools import tools, run_bash_command

    load_dotenv()

    model = os.getenv("LITELLM_MODEL") or "none"
    api_key = os.getenv("LITELLM_API_KEY")

    litellm.suppress_debug_info = True

    with open("prompts/master.txt", "r") as f:
        system_prompt = f.read()

    if len(argv) < 2:
        print("Please enter a prompt")
        return -1
    else:
        user_prompt = argv[1]

    messages: list[Any] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    while True:
        response = litellm.completion(
            model=model,
            api_key=api_key,
            messages=messages,
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

        messages.append(message_dict)

        if not message_obj.tool_calls:
            print(message_obj.content)
            break

        for tool_call in message_obj.tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"--- Running Tool: {function_name} with {args} ---")

            if function_name == "run_bash_command":
                result = run_bash_command(args["command"])
            else:
                result = "Error: Tool not found"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": result,
                }
            )


if __name__ == "__main__":
    main()
