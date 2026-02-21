from pydantic_settings import BaseSettings
from pydantic import ConfigDict



class Settings(BaseSettings):

    model_config = ConfigDict(env_file=".env")

    # for database:
    postgres_user: str 
    postgres_password: str
    postgres_port: int = 5432
    postgres_host: str = "localhost"
    postgres_db_name: str

    # for security:
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def db_url(self):
        return (
            f"postgresql://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db_name}"
        )


app_settings = Settings()
