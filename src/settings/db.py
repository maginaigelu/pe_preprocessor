from pydantic import Field

from settings.base import BaseConfig
from utils import get_env

DB_PREFIX = 'SDB_'
JDBC_PREFIX = 'JDBC_'


class DBConfig(BaseConfig):

    engine: str = Field(get_env(DB_PREFIX, 'ENGINE', 'postgresql'))
    host: str = Field(get_env(DB_PREFIX, 'HOST', 'postgres'))
    port: int = Field(get_env(DB_PREFIX, 'PORT', 5432))
    database: str = Field(get_env(DB_PREFIX, 'DATAbASE', 'pe_preprocessor'))
    username: str = Field(get_env(DB_PREFIX, 'USERNAME', 'pe_preprocessor'))
    password: str = Field(get_env(DB_PREFIX, 'PASSWORD', 'pe_preprocessor'))

    def as_url(self, credentials: bool = False):
        url = f'{self.host}:{self.port}/{self.database}'
        if credentials:
            url = f'{self.username}:{self.password}@{url}'
        url = f'{self.engine}://{url}'
        return url


class JDBCConfig(BaseConfig):

    def as_options(self, **options):
        db_conf = DBConfig()
        db_options = {
            'properties': {
                'user': db_conf.username,
                'password': db_conf.password,
            },
            'url': f'jdbc:{db_conf.as_url()}'
        }
        db_options.update(**options)
        return super(JDBCConfig, self).as_options(**db_options)
