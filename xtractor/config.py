from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Contains all config settings needed throughout the application"""

    X_EMAIL: str
    X_USERNAME: str
    X_PASS: str

    class Config:
        """Environment file where the configs are stored"""

        env_file = ".env"


settings = Settings()
