import os
from pydantic import BaseModel


class Config(BaseModel):
    mistral_api_key: str


def load_config() -> Config:
    env_vars = {}
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                env_vars[key] = value

    mistral_api_key = os.environ.get("MISTRAL_API_KEY") or env_vars.get(
        "MISTRAL_API_KEY", ""
    )

    return Config(mistral_api_key=mistral_api_key)
