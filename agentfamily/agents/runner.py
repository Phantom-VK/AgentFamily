import asyncio
import json
import random

from dotenv import load_dotenv
from agents import ItemHelpers, Runner, set_tracing_disabled
from agents.exceptions import MaxTurnsExceeded

from agentfamily.agents.family import family_agents

# ✅ Setup
load_dotenv()
set_tracing_disabled(True)

TOPIC = "Discuss what to cook for dinner tonight."
MAX_TURNS = 20


def build_input(topic: str, transcript: list[tuple[str, str]]) -> str:
    if transcript:
        last_speaker, last_message = transcript[-1]
        latest_context = (
            f"Last speaker: {last_speaker}\n"
            f"Last message: {last_message}"
        )
    else:
        latest_context = "Last speaker: None\nLast message: This is the start of the conversation."

    return f"""
Simulate a natural family conversation.

Topic: {topic}

Recent context:
{latest_context}

Rules:
- Speak naturally as a family member
- Keep replies short
- Use handoffs between members
- Reach a decision within 4 to 6 exchanges if possible
- If two family members clearly agree, finish the conversation
- Do not hand off more than necessary
- End conversation by calling stop_conversation with a final decision
""".strip()


# ✅ Unified parser (handles both spoken + stop)
def parse_output(output):
    if isinstance(output, dict):
        return output

    if isinstance(output, str):
        try:
            return json.loads(output)
        except:
            return None

    return None


async def run_chat(topic: str = TOPIC):
    starting_agent = random.choice(family_agents)
    current_agent = starting_agent
    transcript: list[tuple[str, str]] = []

    print(f"Starting with: {current_agent.name}\n")

    final_decision = None

    try:
        result = Runner.run_streamed(
            current_agent,
            build_input(topic, transcript),
            max_turns=MAX_TURNS,
        )

        async for event in result.stream_events():

            # 🔹 Handle agent switch
            if event.type == "agent_updated_stream_event":
                prev = current_agent.name
                current_agent = event.new_agent

                if prev != current_agent.name:
                    print(f"[handoff] {prev} -> {current_agent.name}")

            # 🔹 Handle outputs
            elif event.type == "run_item_stream_event":

                if event.item.type == "message_output_item":
                    text = ItemHelpers.text_message_output(event.item).strip()
                    if text:
                        print(f"{current_agent.name}: {text}")

                elif event.item.type == "tool_call_output_item":
                    data = parse_output(event.item.output)

                    if not data:
                        continue

                    # ✅ Spoken message
                    if data.get("status") == "spoken":
                        msg = data.get("message", "").strip()
                        if msg:
                            transcript.append((current_agent.name, msg))
                            print(f"{current_agent.name}: {msg}")

                    # ✅ Final decision
                    elif data.get("status") == "completed":
                        final_decision = data.get("decision")
                        break

        # fallback
        if not final_decision:
            data = parse_output(result.final_output)
            if data and data.get("status") == "completed":
                final_decision = data.get("decision")
    except MaxTurnsExceeded:
        print(f"\nMax turns reached ({MAX_TURNS}). Stopping conversation early.")

    print("\n---")

    if final_decision:
        print(f"Decision: {final_decision}")
    else:
        print("No final decision reached.")

    return final_decision
