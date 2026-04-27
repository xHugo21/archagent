import litellm

from session import Session
from agent import Agent

litellm.suppress_debug_info = True


def main():
    session = Session()
    agent = Agent(session)

    session.run(agent.run)


if __name__ == "__main__":
    main()
