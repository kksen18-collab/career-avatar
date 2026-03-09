from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings
from pathlib import Path


class CareerAvatarSettings(BaseSettings):
    openai_api_key: str
    pushover_user_key: str
    pushover_api_token: str
    pushover_url: str
    name: str
    model: str = "gpt-4o-mini"
    linkedin_pdf_path: Path = Path(__file__).parent / "data/linkedin.pdf"
    summary_path: Path = Path(__file__).parent / "data/summary.txt"

    model_config = {
        "env_file": Path(__file__).parent / ".env",
    }

    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v):
        if not v.startswith("sk-"):
            raise ValueError("invalid openai api key")
        return v


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str
