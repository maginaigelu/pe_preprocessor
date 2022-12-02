import boto3

from settings import S3Config


class S3Client:
    def __init__(self,
                 config=S3Config,
                 client=boto3.client,
                 **options
                 ):
        self.config = config()
        self.client = client(**self.config.as_options(**options))

    def list_objects(self, bucket, **filter_kwargs):
        paginator = self.client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, **filter_kwargs)
        for page in pages:
            yield page
