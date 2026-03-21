from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from agentfamily.prompts import (
    child_instructions,
    daddy_instructions,
    mommy_instructions,
)

DEFAULT_MODEL_NAME = "litellm/deepseek/deepseek-chat"
FAMILY_ROOM_NAME = "Family Room Agent"




def create_family_agent(
    name: str,
    instructions: str,
    handoffs:list,
    handoff_description: str,
    model: str = DEFAULT_MODEL_NAME,
) -> Agent:
    return Agent(
        name=name,
        instructions=instructions,
        handoffs=handoffs,
        handoff_description=handoff_description,
        model=model,
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

family_room_agent = Agent(
    name=FAMILY_ROOM_NAME,
    instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}

You are the routing agent for a simulated family conversation.
Your job is to decide which family member should start the conversation.
Always hand off to exactly one family member.
Do not answer the conversation yourself.
Choose the person whose personality best fits the conversation topic.
""".strip(),
    handoffs=[mommy_agent, daddy_agent, child_agent],
    model=DEFAULT_MODEL_NAME,
)


# Handoffs

mommy_agent.handoffs = [daddy_agent, child_agent]
daddy_agent.handoffs = [mommy_agent, child_agent]
child_agent.handoffs = [mommy_agent, daddy_agent]
