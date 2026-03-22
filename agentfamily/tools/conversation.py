from agents import function_tool
from agentfamily.logger import app_logger


@function_tool
def say_message(message: str):
    """Speak one short line in the family conversation and continue the discussion."""
    app_logger.info(f"say_message called with message='{message}'")
    return {
        "status": "spoken",
        "message": message,
    }


@function_tool
def stop_conversation(decision: str):
    """Stop the family conversation once the family has reached a final decision."""
    app_logger.info(f"stop_conversation called with decision='{decision}'")
    return {
        "status": "completed",
        "decision": decision,
    }
