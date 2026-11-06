from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration lue depuis les variables d'environnement ou le fichier .env."""

    database_url: str = "postgresql+psycopg2://inventaire:inventaire@localhost:5432/inventaire"
    app_name: str = "API Inventaire Informatique"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
