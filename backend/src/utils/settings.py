from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from sqlmodel import Field

class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=str(ENV_PATH),extra='ignore')
    model_config = SettingsConfigDict(env_file='.env',extra='ignore')

    LOGIN_SECRET_KEY:str

    LOGIN_ALGORITHM: str

    TOKEN_EXP_HOURS:int

    DATABASE_URL:str

    ALLOWED_ORIGINS_RAW: str = Field(default="", alias="ALLOWED_ORIGINS")

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]




settings = Settings()