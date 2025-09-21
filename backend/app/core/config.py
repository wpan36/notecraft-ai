import os
from dataclasses import dataclass

def _env(key: str, default: str = "") -> str:
    val = os.getenv(key)
    return val if val is not None and val != "" else default

@dataclass
class Settings:
    DATABASE_URL: str = _env(
        "DATABASE_URL",
        "postgresql://notecraft:notecraft@db:5432/notecraft",
    )
    APP_ENV: str = _env("APP_ENV", "dev")

settings = Settings()
