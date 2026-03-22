import asyncio

from agentfamily.agents.runner import run_chat

def main():
    asyncio.run(run_chat(topic="What to make today?"))

if __name__ == "__main__":
    main()