import json
from career_avatar.tools.record_unknown_question import record_unknown_question_json
from career_avatar.tools.record_user_details import record_user_details_json
from career_avatar.client.pushover import PushoverClient

import logging

logger = logging.getLogger(__name__)


class Tools:
    def __init__(self, *, pushover_client: PushoverClient):
        self.pushover_client = pushover_client

    @property
    def tool_definition(self) -> list[dict[str, str]]:
        tools = [
            {"type": "function", "function": record_user_details_json},
            {"type": "function", "function": record_unknown_question_json},
        ]
        logger.debug("Tool definition: %s", tools)
        return tools

    def _record_user_details(
        self,
        *,
        email: str,
        name: str = "Name not provided",
        notes: str = "not provided",
    ) -> dict[str, str]:
        self.pushover_client.push(
            f"Recording interest from {name} with email {email} and notes {notes}"
        )
        return {"recorded": "ok"}

    def _record_unknown_question(self, *, question: str) -> dict[str, str]:
        self.pushover_client.push(f"Recording {question} asked that I couldn't answer")
        return {"recorded": "ok"}

    def handle_tool_calls(self, tool_calls: list) -> list[dict[str, str]]:
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            logger.info("Tool called %s", tool_name)

            if tool_name == "record_user_details":
                result = self._record_user_details(**arguments)
            elif tool_name == "record_unknown_question":
                result = self._record_unknown_question(**arguments)
            else:
                result = {"error": f"unknown tool: {tool_name}"}

            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
            logger.debug("Tool result: %s", result)
        return results
