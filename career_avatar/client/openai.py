import logging
from typing import TypeVar

from openai import NOT_GIVEN, OpenAI
from openai._types import NotGiven
from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion import Choice
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def create_chat_completion(
        self,
        *,
        model: str,
        messages: list,
        tools: list[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
    ) -> Choice:
        response = self.client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
        logger.debug("OpenAI response: %s", response)
        return response.choices[0]

    def parse(
        self, *, model: str, messages: list, response_format: type[T]
    ) -> T | None:
        response = self.client.responses.parse(
            model=model, input=messages, text_format=response_format
        )
        logger.debug("Parse response: %s", response)
        result = response.output_parsed
        if result is None:
            raise ValueError("Parse returned no output")
        return result
