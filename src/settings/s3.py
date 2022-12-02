from typing import Any

from botocore import UNSIGNED
from botocore.config import Config
from pydantic import Field

from settings.base import BaseConfig
from utils import get_env

S3_PREFIX = 'S3_'


class S3Options(BaseConfig):

    signature_version: Any = Field(get_env(S3_PREFIX, 'SIGNATURE_VERSION', UNSIGNED))

    def as_options(self, **options):
        return Config(**super(S3Options, self).as_options(**options))


class S3Config(BaseConfig):

    service_name: str = Field('s3')
    region_name: str = Field(get_env(S3_PREFIX, 'REGION', 'eu-central-1'))
    config: Any = Field(S3Options().as_options())
