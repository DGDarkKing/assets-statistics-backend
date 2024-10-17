from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False

    db_app_max_pool: int = Field(gt=0, default=10)
    db_app_overflow_pool: int = Field(gt=0, default=15)
    db_host: str
    db_port: int = Field(gt=0)
    db_user: str
    db_pass: str
    db_name: str

    mq_url: str
    rabbitmq_publish_exchange: str
    mq_user: str
    mq_pass: str

    s3_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_secure: bool = False

    @property
    def db_async_url(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'


app_settings = AppSettings(
    _env_file=[
        f'{__file__}/../../envs/prod.env',
        f'{__file__}/../../envs/dev.env',
    ],
    _env_file_encoding='utf-8'
)

