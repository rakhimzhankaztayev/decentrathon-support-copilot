"""Application configuration loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Runtime settings for the API and batch inference."""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Grand Support Copilot"
    data_dir: Path = ROOT_DIR / "data"
    rules_file: str = "rules.json"
    taxonomy_file: str = "taxonomy.json"
    confidence_threshold: float = 0.65
    duplicate_similarity_threshold: float = 0.88
    max_retrieved_documents: int = 5

    @property
    def rules_path(self) -> Path:
        return self.data_dir / self.rules_file

    @property
    def taxonomy_path(self) -> Path:
        return self.data_dir / self.taxonomy_file


@lru_cache
def get_settings() -> Settings:
    return Settings()
