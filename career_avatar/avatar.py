import logging
from pathlib import Path

from career_avatar.client.openai import OpenAIClient
from career_avatar.evaluation import Evaluator
from career_avatar.loader import Loader
from career_avatar.prompt import PromptBuilder
from career_avatar.tools.tools import Tools

logger = logging.getLogger(__name__)


class Avatar:
    def __init__(
        self,
        *,
        name: str,
        openai_client: OpenAIClient,
        tools: Tools,
        loader: Loader,
        linkedin_pdf_path: Path,
        summary_path: Path,
        model: str,
    ):
        self.openai_client = openai_client
        self.tools = tools
        self.model = model
        self.prompt_builder = PromptBuilder(
            name=name,
            summary=loader.load_txt(summary_path),
            linkedin=loader.load_pdf(linkedin_pdf_path),
        )
        self.evaluator = Evaluator(
            openai_client=openai_client, prompt_builder=self.prompt_builder
        )

    def chat(self, message: str, history: list) -> str | None:
        messages = (
            [{"role": "system", "content": self.prompt_builder.system_prompt()}]
            + history
            + [{"role": "user", "content": message}]
        )
        done = False
        while not done:
            choice = self.openai_client.create_chat_completion(
                model=self.model,
                messages=messages,
                tools=self.tools.tool_definition,
            )
            logger.debug("OpenAI response: %s", choice)
            if choice.finish_reason == "tool_calls":
                tool_calls = choice.message.tool_calls
                results = self.tools.handle_tool_calls(tool_calls)
                messages.append(choice.message)
                messages.extend(results)
                logger.debug("messages after tool calls: %s", messages)
            else:
                done = True
        reply = choice.message.content
        if reply is None:
            logger.warning("No content in reply")
            return None
        evaluation = self.evaluator.evaluate(
            model=self.model, reply=reply, message=message, history=history
        )
        if evaluation.is_acceptable:
            logger.info("Passed evaluation - returning reply")
            logger.debug("Final response: %s", reply)
            return reply
        else:
            logger.info("Failed evaluation - retrying")
            logger.info(evaluation.feedback)
            reply = self.evaluator.rerun(
                model=self.model,
                reply=reply,
                message=message,
                history=history,
                feedback=evaluation.feedback,
            )

            return reply
