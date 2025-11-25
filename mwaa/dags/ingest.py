from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models.param import Param

# Define DAG params using Param
DATA_LAKE_HOST_PATH = Param(
    default="/Users/loubrieu/Documents/edrn/labcas_local",
    description="file path where the archive data, metadata, thumbnails, etc. are stored, as mounted inside the Docker container",
    type="string"
)
DATA_STAGE_HOST_PATH = Param(
    default="/Users/loubrieu/Documents/edrn/labcas_stage",
    description="file path where the staging data is stored, as mounted inside the Docker container",
    type="string"
)
SOLR_URL = Param(
    default="http://solr:8983/solr/",
    description="URL for the Solr instance",
    type="string"
)
USERNAME = Param(
    default="thomas",
    description="Username for the process (if needed)",
    type="string"
)
PUBLISH_ARGS = Param(
    default="--collection Autoantibody_Biomarkers --steps headers hash crawl updown compare publish",
    description="Arguments to override the Docker CMD",
    type="string"
)

# Define default_args for the DAG
default_args = {
    'data_lake_host_path': DATA_LAKE_HOST_PATH,
    'data_stage_host_path': DATA_STAGE_HOST_PATH,
    'solr_url': SOLR_URL,
    'username': USERNAME,
    'publish_args': PUBLISH_ARGS,
}

# Instantiate the DAG
with DAG(
    dag_id='ingest_dag',
    default_args=default_args,
    description='A simple ingest DAG',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['example'],
    params={
        'data_lake_host_path': DATA_LAKE_HOST_PATH,
        'data_stage_host_path': DATA_STAGE_HOST_PATH,
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
        command=dag.params['publish_args'],  # Override CMD with publish_args param
        docker_url='unix://var/run/docker.sock',
        mounts=[
            Mount("/data_lake", dag.params['data_lake_host_path'], type='bind'),
            Mount("/data_stage", dag.params['data_stage_host_path'], type='bind'),
        ],
        environment={
            'solr': dag.params['solr_url'],
            'username': dag.params['username'],
        }
    )
    # Add more tasks or dependencies as needed
