"""
AR: إعدادات التطبيق تُقرأ من متغيرات البيئة (أو ملف `.env`).
EN: Application settings loaded from environment variables (and optional `.env` file).

لماذا نستخدم Pydantic Settings؟ / Why Pydantic Settings?
- Typing + validation for env vars
- `.env` support for local development
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    AR: كل الحقول هنا يمكن ضبطها من `.env` بنفس الاسم بأحرف كبيرة (DATABASE_URL).
    EN: Fields map to env vars with the same name in UPPER_SNAKE_CASE by default.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./ecommerce.db"
    secret_key: str = "mysecret123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # AR: نخزنها كنص ثم نحوّلها لقائمة — أسهل من قائمة في ملف `.env`
    # EN: Store as string, convert to list — easier than list syntax in `.env`
    cors_origins: str = "*"

    @property
    def cors_origins_list(self) -> list[str]:
        """AR/EN: `*` أو قائمة عناوين مفصولة بفواصل."""
        raw = self.cors_origins.strip()
        if raw == "*":
            return ["*"]
        return [part.strip() for part in raw.split(",") if part.strip()]


# AR: كائن واحد نستوردُه في بقية المشروع
# EN: Single settings instance imported across the app
settings = Settings()
