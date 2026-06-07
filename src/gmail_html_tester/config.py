import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    sender_email: str
    app_password: str
    receiver_email: str
    gemini_api_key: str
    use_gemini: bool

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            sender_email=os.getenv("SENDER_EMAIL", ""),
            app_password=os.getenv("APP_PASSWORD", ""),
            receiver_email=os.getenv("RECEIVER_EMAIL", ""),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            use_gemini=os.getenv("USE_GEMINI", "false").lower() == "true",
        )

    @property
    def smtp_ready(self) -> bool:
        return all([self.sender_email, self.app_password, self.receiver_email])

    @property
    def gemini_ready(self) -> bool:
        return self.use_gemini and bool(self.gemini_api_key)


settings = Settings.load()
