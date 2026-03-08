import gradio as gr
from career_avatar.parameters import CareerAvatarSettings
from career_avatar.client.openai import OpenAIClient
from career_avatar.client.pushover import PushoverClient
from career_avatar.tools.tools import Tools
from career_avatar.loader import Loader
from career_avatar.avatar import Avatar


def main():
    settings = CareerAvatarSettings()  # type: ignore

    openai_client = OpenAIClient(api_key=settings.openai_api_key)
    pushover_client = PushoverClient(
        token=settings.pushover_api_token,
        user_key=settings.pushover_user_key,
        url=settings.pushover_url,
    )
    tools = Tools(pushover_client=pushover_client)
    loader = Loader()
    avatar = Avatar(
        name=settings.name,
        openai_client=openai_client,
        tools=tools,
        loader=loader,
        linkedin_pdf_path=settings.linkedin_pdf_path,
        summary_path=settings.summary_path,
        model=settings.model,
    )

    gr.ChatInterface(avatar.chat).launch()


if __name__ == "__main__":
    main()
