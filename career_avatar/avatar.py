from career_avatar.client.openai import OpenAIClient
from career_avatar.tools.tools import Tools
from career_avatar.prompt import PromptBuilder
from career_avatar.loader import Loader
from pathlib import Path


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

    def chat(self, message: str, history: list) -> str | None:
        messages = (
            [{"role": "system", "content": self.prompt_builder.build()}]
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
            if choice.finish_reason == "tool_calls":
                tool_calls = choice.message.tool_calls
                results = self.tools.handle_tool_calls(tool_calls)
                messages.append(choice.message)
                messages.extend(results)
            else:
                done = True
        return choice.message.content
