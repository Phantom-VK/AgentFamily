from agents import Agent, ModelSettings, StopAtTools
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from agentfamily.prompts import (
    child_instructions,
    daddy_instructions,
    mommy_instructions,
)
from agentfamily.logger import app_logger
from agentfamily.tools import say_message, stop_conversation

DEFAULT_MODEL_NAME = "litellm/deepseek/deepseek-chat"
MEMBER_MODEL_SETTINGS = ModelSettings(
    max_tokens=64,
    temperature=0.4,
    parallel_tool_calls=False,
)

app_logger.info(f"Initializing family agents with model '{DEFAULT_MODEL_NAME}'")


def _build_member_instructions(instructions: str) -> str:
    return f"""
{RECOMMENDED_PROMPT_PREFIX}

You are a family member in a live conversation.

STRICT RULES (must follow exactly):

1. You must ALWAYS respond using a tool.
   - To speak → call `say_message`
   - To end → call `stop_conversation`
   - Never output plain text

2. Conversation flow:
   - First: call `say_message` with your reply (1–2 short sentences)
   - Then:
       - If conversation should continue → hand off to another agent
       - If final decision is reached → call `stop_conversation`

3. Handoffs:
   - Always choose the most appropriate next family member
   - Do NOT explain the handoff
   - Do NOT speak again after handing off

4. stop_conversation:
   - Only call when a clear final decision is reached
   - Pass ONLY a short plain string (no JSON, no quotes, no formatting)

5. Style rules:
   - No speaker labels
   - No narration
   - No explanations of actions
   - Stay fully in character

6. Hard constraints:
   - Never skip `say_message` before handoff
   - Never return raw text
   - Never call multiple tools in one turn
   - Never loop unnecessarily

Failure to follow rules = incorrect behavior.

{instructions.strip()}
""".strip()


def create_family_agent(
    name: str,
    instructions: str,
    handoff_description: str,
    model: str = DEFAULT_MODEL_NAME,
) -> Agent:
    return Agent(
        name=name,
        instructions=_build_member_instructions(instructions),
        handoff_description=handoff_description,
        model=model,
        model_settings=MEMBER_MODEL_SETTINGS,
        tools=[say_message, stop_conversation],
        tool_use_behavior=StopAtTools(stop_at_tool_names=["stop_conversation"]),
    )


mommy_agent = create_family_agent(
    name="Mommy Agent",
    instructions=mommy_instructions,
    handoff_description="Best for warmth, emotions, food, home matters, and calm family guidance.",
)
daddy_agent = create_family_agent(
    name="Daddy Agent",
    instructions=daddy_instructions,
    handoff_description="Best for practical decisions, money, gadgets, planning, and protective family advice.",
)
child_agent = create_family_agent(
    name="Child Agent",
    instructions=child_instructions,
    handoff_description="Best for playful reactions, school-life perspective, fun ideas, and youthful curiosity.",
)

family_agents = [mommy_agent, daddy_agent, child_agent]


# Handoffs
mommy_agent.handoffs = [daddy_agent, child_agent]
daddy_agent.handoffs = [mommy_agent, child_agent]
child_agent.handoffs = [mommy_agent, daddy_agent]
app_logger.info("Family agents and peer handoffs initialized")
