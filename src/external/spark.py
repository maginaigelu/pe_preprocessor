import pyspark
from pyspark.sql.functions import col

from settings.db import JDBCConfig
from settings.spark import SparkConfig, S3SparkConfig
from utils import hash_it, get_pe_meta


class BasePySparkClient:

    def __init__(self, *,
                 config=SparkConfig,
                 builder=pyspark.sql.SparkSession.builder,
                 **options
                 ):
        self.config = config()
        self.builder = builder
        for key, value in self.config.as_options(**options).items():
            self.builder.config(key, value)

    @property
    def get_session(self):
        return self.builder.getOrCreate()

    @staticmethod
    def get_jdbc(df, **options):
        return df.jdbc(**JDBCConfig().as_options(**options))

    # ETL
    def process_tasks(self, list_tasks, result_table_name, *fields, hash_field='hash', mode='append'):
        df = self.get_session
        extracted = self.extract(df, list_tasks)
        transformed = self.transform(extracted, table_name=result_table_name, fields=fields, hash_field=hash_field)
        loaded = self.load(transformed, result_table_name, mode=mode)
        df.stop()
        return loaded

    @staticmethod
    def extract(df, list_tasks, fmt='binaryFile'):
        return df.read.format(fmt).load(list_tasks)

    def transform(self, df, *, table_name, fields, hash_field='hash'):
        df = df.withColumn(hash_field, hash_it(col('content'))).dropDuplicates([hash_field])
        df = self.clean_duplicates_from_jdbc(df, table_name, hash_field)
        df = df.withColumn('meta', get_pe_meta(col('content'))).select(
            hash_field, 'meta.architecture', 'meta.file_type', 'meta.imports', 'meta.exports', *fields
        )
        return df

    def clean_duplicates_from_jdbc(self, df, table_name, index_field):
        df2 = self.get_jdbc(
            self.get_session.read,
            table=table_name,
        ).filter(col(index_field).isin(df.select(index_field).rdd.flatMap(lambda x: x).collect()))
        return df.join(df2, [index_field], "leftanti")

    def load(self, df, table_name, mode='append'):
        return self.get_jdbc(df.write, table=table_name, mode=mode)


class S3SparkClient(BasePySparkClient):

    def __init__(self, *,
                 config=S3SparkConfig,
                 **options):
        super(S3SparkClient, self).__init__(config=config, **options)
