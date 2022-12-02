import dramatiq
from dramatiq import actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from external.s3 import S3Client
from external.spark import S3SparkClient
from models import FilesMetadata, Task
from models.base import SessionLocal
from settings.amqp import AmqpConfig
from utils import transform_s3_page

broker = RabbitmqBroker(url=AmqpConfig().as_url())
dramatiq.set_broker(broker)


def set_status_operation(func, task_id, *args, **kwargs):
    status = 'Done'
    try:
        return func(*args, **kwargs)
    except:
        status = 'Failed'
        raise
    finally:
        with SessionLocal() as session:
            session.query(Task).filter(Task.id == task_id).update({Task.status: status})
            session.commit()


def _process_pe_from_s3(bucket, cnt, page_size):
    client = S3Client()
    prefixes = []
    for page in client.list_objects(bucket, Delimiter='/'):
        prefixes.extend(page['CommonPrefixes'])
    files_count_per_directory = int(cnt / len(prefixes)) or 1
    for prefix in prefixes:
        prefix_pages = client.list_objects(
            bucket,
            PaginationConfig={'MaxItems': files_count_per_directory, 'PageSize': page_size},
            **prefix
        )
        for page in prefix_pages:
            _preprocess_pe_files(transform_s3_page(page['Contents'], bucket))


@actor(time_limit=10800000)
def process_pe_from_s3(bucket, cnt, page_size, task_id):
    return set_status_operation(_process_pe_from_s3, task_id, bucket, cnt, page_size)


def _preprocess_pe_files(list_tasks):
    spark_client = S3SparkClient()
    return spark_client.process_tasks(list_tasks, FilesMetadata.__table__.name, 'path', 'length')


@actor(time_limit=10800000)
def preprocess_pe_files(list_tasks, task_id):
    return set_status_operation(_preprocess_pe_files, task_id, list_tasks)
