def main():
    import os
    from dotenv import load_dotenv
    from typing import cast
    import litellm

    load_dotenv()

    model = os.getenv("LITELLM_MODEL") or "none"
    api_key = os.getenv("LITELLM_API_KEY")

    litellm.suppress_debug_info = True

    with open("prompts/master.txt", "r") as f:
        system_prompt = f.read()

    user_prompt = "Who are you"

    response = litellm.completion(
        model=model,
        api_key=api_key,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=False,
    )

    response = cast(litellm.ModelResponse, response)

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
