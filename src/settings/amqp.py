from pydantic import Field

from settings.base import BaseConfig
from utils import get_env

AMQP_PREFIX = 'AMQP_'


class AmqpConfig(BaseConfig):
    user: str = Field(get_env(AMQP_PREFIX, 'USER', 'rabbitmq'))
    password: str = Field(get_env(AMQP_PREFIX, 'PASSWORD', 'rabbitmq'))
    host: str = Field(get_env(AMQP_PREFIX, 'HOST', 'rabbitmq'))
    port: int = Field(get_env(AMQP_PREFIX, 'PORT', 5672))
    vhost: str = Field(get_env(AMQP_PREFIX, 'VHOST', 'rabbitmq'))

    def as_url(self):
        return f'amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}'