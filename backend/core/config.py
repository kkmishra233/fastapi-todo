from os import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class BaseProjectSettings(BaseSettings):
    PROJECT_TITLE: str = ""
    PROJECT_VERSION: str = ""
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/db.sqlite3"
    LOG_FILE: str = f"{BASE_DIR}/app.log"
    LOG_LEVEL: str = "INFO"

class DevProjectSettings(BaseProjectSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env.dev"))

class StageProjectSettings(BaseProjectSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env.stg"))

class PrdProjectSettings(BaseProjectSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env.prd"))

def get_project_settings(env: str) -> BaseProjectSettings:
    settings_config_dictionary = {
        "development": DevProjectSettings,
        "staging": StageProjectSettings,
        "production": PrdProjectSettings
    }
    settings_class = settings_config_dictionary.get(env, DevProjectSettings)  # Default to dev
    return settings_class()

env = getenv("APP_ENV", "development").lower()
settings = get_project_settings(env)
