import logging

from career_avatar.client.openai import OpenAIClient
from career_avatar.parameters import Evaluation
from career_avatar.prompt import PromptBuilder

logger = logging.getLogger(__name__)


class Evaluator:
    def __init__(
        self,
        openai_client: OpenAIClient,
        prompt_builder: PromptBuilder,
    ):
        self.openai_client = openai_client
        self.prompt_builder = prompt_builder

    def evaluate(
        self, model: str, reply: str, message: str, history: list
    ) -> Evaluation | None:
        messages = [
            {"role": "system", "content": self.prompt_builder.evaluator_system_prompt}
        ] + [
            {
                "role": "user",
                "content": self.prompt_builder.evaluator_user_prompt(
                    reply, message, history
                ),
            }
        ]
        response = self.openai_client.parse(
            model=model, messages=messages, response_format=Evaluation
        )
        logger.debug("Evaluation response: %s", response)
        return response

    def rerun(
        self, model: str, reply: str | None, message: str, history: list, feedback: str
    ) -> str | None:
        updated_system_prompt = (
            self.prompt_builder.evaluator_system_prompt
            + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        )
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        messages = (
            [{"role": "system", "content": updated_system_prompt}]
            + history
            + [{"role": "user", "content": message}]
        )
        choice = self.openai_client.create_chat_completion(
            model=model, messages=messages
        )
        return choice.message.content
