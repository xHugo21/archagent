import os
from dotenv import load_dotenv
import litellm
from ui import InteractiveSession
from agent import Agent

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


def main():
    model, api_key = get_env_vars()
    messages = initialize_messages()

    session = InteractiveSession(messages)
    agent = Agent(model, api_key, session)

    session.run(agent.run)


if __name__ == "__main__":
    main()
