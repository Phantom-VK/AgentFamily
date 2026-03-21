


from __future__ import annotations

import argparse
import os

from agents import RunHooks, Runner, set_tracing_disabled

from agentfamily.agents.family import family_room_agent

DEFAULT_TOPIC = "Discuss what to cook for dinner tonight."
DEFAULT_TURNS = 6

FAMILY_CHAT_RULES = """
You are participating in a live family conversation.

Conversation rules:
- One family member should speak next.
- If you are the family room router, hand off to the best family member.
- Speak naturally to the other family members, not to the system.
- Reply in 1 to 3 short sentences.
- React to the latest message and keep the conversation moving.
- Sound like a real family member talking at home.
- Do not mention being an AI, an agent, a model, or a prompt.
- Do not add a speaker label like "Mommy:" because the runner prints that already.
""".strip()


def configure_runtime() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        set_tracing_disabled(True)


def _format_transcript(transcript: list[tuple[str, str]]) -> str:
    if not transcript:
        return "No one has spoken yet."

    return "\n".join(f"{speaker.title()}: {message}" for speaker, message in transcript)


def _build_turn_input(
    topic: str,
    transcript: list[tuple[str, str]],
) -> str:
    if transcript:
        latest_speaker, latest_message = transcript[-1]
        latest_line = f"The latest message was from {latest_speaker.title()}: {latest_message}"
    else:
        latest_line = "This is the first turn. Start the family conversation naturally."

    return f"""
{FAMILY_CHAT_RULES}

Topic:
{topic}

Conversation so far:
{_format_transcript(transcript)}

{latest_line}
Choose the best next family speaker and continue the conversation.
""".strip()


class FamilyConversationHooks(RunHooks):
    async def on_handoff(self, from_agent, to_agent) -> None:
        print(f"[handoff] {from_agent.name} -> {to_agent.name}")


def simulate_family_chat(
    topic: str = DEFAULT_TOPIC,
    turns: int = DEFAULT_TURNS,
) -> list[tuple[str, str]]:
    configure_runtime()

    transcript: list[tuple[str, str]] = []

    for _ in range(turns):
        turn_input = _build_turn_input(topic, transcript)
        result = Runner.run_sync(
            family_room_agent,
            turn_input,
            hooks=FamilyConversationHooks(),
        )
        speaker = result.last_agent.name
        message = str(result.final_output).strip()
        transcript.append((speaker, message))
        print(f"{speaker}: {message}")

    return transcript


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate a family conversation.")
    parser.add_argument(
        "--topic",
        default=DEFAULT_TOPIC,
        help="Topic for the family to discuss.",
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=DEFAULT_TURNS,
        help="How many family replies to simulate.",
    )
    args = parser.parse_args()

    simulate_family_chat(topic=args.topic, turns=args.turns)


if __name__ == "__main__":
    main()
