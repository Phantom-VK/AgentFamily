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

You are in a live family discussion.
Never reply with plain assistant text.
When you want to speak, you must call `say_message`.
After `say_message`, either hand off to another family member or call `stop_conversation`.
Speak in 1 or 2 short sentences.
If another family member should respond next, hand off to them.
If the family has reached a clear final decision, call `stop_conversation`.
When calling `stop_conversation`, pass only one short plain-text decision string.
Do not include nested quotes, markdown, or JSON inside tool arguments.
Do not add speaker labels or extra narration.
Do not break character.

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
