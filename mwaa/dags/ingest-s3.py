import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models.param import Param

# Mount points can't be templated, must be statically loaded

DEFAULT_DATA_LAKE_HOST_PATH = '/labcas_local'
DEFAULT_DATA_STAGE_HOST_PATH = '/labcas_stage'
DEFAULT_DATA_STAGE_CONTAINER_PATH = '/data_stage'

DATA_LAKE_HOST_PATH = os.getenv('AIRFLOW_VAR_DATA_LAKE_HOST_PATH', DEFAULT_DATA_LAKE_HOST_PATH)
DATA_STAGE_HOST_PATH = os.getenv('AIRFLOW_VAR_DATA_STAGE_HOST_PATH', DEFAULT_DATA_STAGE_HOST_PATH)

DEFAULT_SOLR_URL = "http://solr:8983/solr/"
DEFAULT_USERNAME = "thomas"
DEFAULT_PUBLISH_ARGS = "--collection Autoantibody_Biomarkers --steps headers hash crawl updown compare publish"
DEFAULT_COLLECTION_ARCHIVE_BUCKET_URI="s3://edrn-labcas/archive"
DEFAULT_COLLECTION="Autoantibody_Biomarkers"

# Define DAG params using Param
SOLR_URL = Param(
    DEFAULT_SOLR_URL,
    description="URL for the Solr instance",
    type="string"
)
USERNAME = Param(
    DEFAULT_USERNAME,
    description="Username for the process (if needed)",
    type="string"
)
PUBLISH_ARGS = Param(
    DEFAULT_PUBLISH_ARGS,
    description="Arguments to override the Docker CMD",
    type="string"
)

COLLECTION_ARCHIVE_BUCKET = Param(
    DEFAULT_COLLECTION_ARCHIVE_BUCKET_URI,
    description="S3 Archive Bucket URI",
    type="string"
)

COLLECTION = Param(
    DEFAULT_COLLECTION,
    description="Autoantibody_Biomarkers",
    type="string"
)

# Define default_args for the DAG
default_args = {
    'data_lake_host_path': DATA_LAKE_HOST_PATH,
    'data_stage_host_path': DATA_STAGE_HOST_PATH,
    'solr_url': DEFAULT_SOLR_URL,
    'username': DEFAULT_USERNAME,
    'publish_args': DEFAULT_PUBLISH_ARGS,
    "archive_bucket_uri": COLLECTION_ARCHIVE_BUCKET,
    "collection": COLLECTION,
    "container_data_lake_path": DEFAULT_DATA_STAGE_CONTAINER_PATH
}
# Instantiate the DAG
with DAG(
    dag_id='ingest_dag_s3',
    description='A simple ingest DAG',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['example'],
    params={
        'solr_url': SOLR_URL,
        'username': USERNAME,
        'publish_args': PUBLISH_ARGS,
        'collection_archive_bucket_s3uri': COLLECTION_ARCHIVE_BUCKET,
        'collection': COLLECTION
    },
) as dag:
    publish_task = DockerOperator(
        task_id='publish_task',
        image='labcas/publish:aws-latest',
        network_mode='labcas',
        api_version='auto',
        auto_remove=True,
        command="{{ params.publish_args }}",  # Override CMD with publish_args param
        docker_url='unix://var/run/docker.sock',
        mounts = [
            Mount(target="/data_lake", source=DATA_LAKE_HOST_PATH, type='bind'),
        ],
        environment={
            'solr': "{{ params.solr_url }}",
            'username': "{{ params.username }}",
            'COLLECTION_ARCHIVE_BUCKET_URI': "{{ params.collection_archive_bucket_s3uri }}",
            'COLLECTION': "{{ params.collection }}",
            'PUBLISH_DATA_STAGE': DEFAULT_DATA_STAGE_CONTAINER_PATH,
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'AWS_SESSION_TOKEN': os.getenv('AWS_SESSION_TOKEN'),
            'AWS_DEFAULT_REGION': 'us-west-2'
        }
    )
    # Add more tasks or dependencies as needed
