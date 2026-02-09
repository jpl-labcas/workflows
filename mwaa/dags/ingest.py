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

DATA_LAKE_HOST_PATH = os.getenv('AIRFLOW_VAR_DATA_LAKE_HOST_PATH', DEFAULT_DATA_LAKE_HOST_PATH)
DATA_STAGE_HOST_PATH = os.getenv('AIRFLOW_VAR_DATA_STAGE_HOST_PATH', DEFAULT_DATA_STAGE_HOST_PATH)

DEFAULT_SOLR_URL = "http://solr:8983/solr/"
DEFAULT_USERNAME = "thomas"
DEFAULT_PUBLISH_ARGS = "--collection Autoantibody_Biomarkers --steps headers hash crawl updown compare publish"

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

# Define default_args for the DAG
default_args = {
    'data_lake_host_path': DATA_LAKE_HOST_PATH,
    'data_stage_host_path': DATA_STAGE_HOST_PATH,
    'solr_url': DEFAULT_SOLR_URL,
    'username': DEFAULT_USERNAME,
    'publish_args': DEFAULT_PUBLISH_ARGS,
}

# Instantiate the DAG
with DAG(
    dag_id='ingest_dag',
    description='A simple ingest DAG',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['example'],
    params={
        'solr_url': SOLR_URL,
        'username': USERNAME,
        'publish_args': PUBLISH_ARGS,
    },
) as dag:
    publish_task = DockerOperator(
        task_id='publish_task',
        image='labcas/publish:latest',
        network_mode='labcas',
        api_version='auto',
        auto_remove=True,
        command="{{ params.publish_args }}",  # Override CMD with publish_args param
        docker_url='unix://var/run/docker.sock',
        mounts = [
            Mount(target="/data_lake", source=DATA_LAKE_HOST_PATH, type='bind'),
            Mount(target="/data_stage", source=DATA_STAGE_HOST_PATH, type='bind'),
        ],
        environment={
            'solr': "{{ params.solr_url }}",
            'username': "{{ params.username }}",
        }
    )
    # Add more tasks or dependencies as needed
