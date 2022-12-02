from pydantic import Field

from settings import S3Config
from settings.base import BaseConfig
from utils import get_env

SPARK_PREFIX = 'SPARK_'
S3A_PREFIX = 'S3A_'


class SparkConfig(BaseConfig):

    master: str = Field(get_env(SPARK_PREFIX, 'MASTER_URL', 'spark://pyspark:7077'), alias='spark.master')
    app_name: str = Field(get_env(SPARK_PREFIX, 'APP_NAME', 'Pe preprocessor'), alias='spark.app.name', )
    executor_memory: str = Field(
        get_env(SPARK_PREFIX, 'EXECUTOR_MEMORY', '2g'), alias='spark.executor.memory'
    )
    executor_cores: str = Field(get_env(SPARK_PREFIX, 'EXECUTOR_CORES', '4'), alias='spark.executor.cores')


class S3SparkConfig(SparkConfig):
    creds_provider: str = Field(
        get_env(S3A_PREFIX, 'CREDENTIALS_PROVIDER', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider'),
        alias='fs.s3a.aws.credentials.provider'
    )

    def as_options(self, **options):
        s3_config = S3Config()
        s3_options = {
            'fs.s3a.endpoint.region': s3_config.region_name,
        }
        s3_options.update(**options)
        return super(S3SparkConfig, self).as_options(**s3_options)
