from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=str(ENV_PATH),extra='ignore')
    model_config = SettingsConfigDict(env_file='.env',extra='ignore')

    LOGIN_SECREATE_KEY:str

    LOGIN_ALGORITHM: str

    TOKEN_EXP_HOURS:int


settings = Settings()