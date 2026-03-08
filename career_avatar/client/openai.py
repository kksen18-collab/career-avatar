from openai import OpenAI
from openai.types.chat.chat_completion import Choice


class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def create_chat_completion(
        self, *, model: str, messages: list, tools: list
    ) -> Choice:
        response = self.client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
        return response.choices[0]
