# AgentFamily

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI-Agents%20SDK-412991?logo=openai&logoColor=white)
![DeepSeek](https://img.shields.io/badge/Model-DeepSeek%20Chat-1F6FEB)
![LiteLLM](https://img.shields.io/badge/Provider-LiteLLM-FF6B35)
![Status](https://img.shields.io/badge/Status-Practice%20Project-2EA44F)

Small practice project for learning agentic AI with the OpenAI Agents SDK. The app simulates a family conversation where three agents talk to each other using handoffs, speak through tools, and stop once they reach a decision.

## What It Does

- Creates three family-member agents: mother, father, and child.
- Starts the conversation with one random family member.
- Lets agents hand off the discussion to each other.
- Uses a `say_message` tool for spoken lines.
- Uses a `stop_conversation` tool to end the run with a final decision.
- Writes runtime logs to the `logs/` directory with timestamped filenames.

## Tech Stack

- Python 3.12+
- OpenAI Agents SDK
- LiteLLM model routing
- DeepSeek Chat model
- `python-dotenv` for local environment loading

## Project Structure

```text
agentfamily/
├── agents/
│   ├── family.py
│   ├── runner.py
│   └── __init__.py
├── prompts/
│   ├── agent_instructions.py
│   └── __init__.py
├── tools/
│   ├── conversation.py
│   └── __init__.py
├── logger.py
└── __init__.py
main.py
pyproject.toml
```

## How It Works

1. `main.py` starts the async conversation runner.
2. `runner.py` picks a random starting family agent.
3. Each agent must speak via the `say_message` tool.
4. After speaking, an agent either hands off to another family member or ends the discussion with `stop_conversation`.
5. The runner prints the conversation and final decision.
6. The logger stores execution details in `logs/agentfamily_YYYY-MM-DD_HH-MM-SS.log`.

## Setup

Create a `.env` file in the project root:

```env
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

Install dependencies in your environment:

```bash
pip install -e .
```

## Run

The current entrypoint is `main.py`:

```python
import asyncio

from agentfamily.agents.runner import run_chat


def main():
    asyncio.run(run_chat(topic="What to make today?"))


if __name__ == "__main__":
    main()
```

Run it however you normally launch Python locally or from your IDE.

## Current Behavior

- The conversation begins with a random family member.
- Handoffs are peer-to-peer only; there is no router agent.
- The run ends when an agent calls `stop_conversation`.
- Logs are kept on disk for debugging SDK events and tool behavior.

## Notes

- This is a practice sandbox, not a production agent system.
- Tool-call formatting can still be sensitive to model behavior.
- The prompt and tool setup are intentionally simple so the handoff flow is easy to inspect and change.
