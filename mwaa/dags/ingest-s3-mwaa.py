import os
from airflow import DAG
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator # Pinned to verion 9.0.0
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models.param import Param

# Mount points can't be templated, must be statically loaded


DEFAULT_DATA_LAKE_HOST_PATH = '/labcas_local'
DEFAULT_DATA_STAGE_HOST_PATH = '/labcas_stage'
DEFAULT_DATA_STAGE_CONTAINER_PATH = '/data_stage'

# Path to local directory where the data archive resides
# not used for this dag
DATA_LAKE_HOST_PATH = os.getenv('AIRFLOW_VAR_DATA_LAKE_HOST_PATH', DEFAULT_DATA_LAKE_HOST_PATH)

# Path to local directory to serve as the data staging area. The publish container will copy S3
# buckets to this location.
DATA_STAGE_HOST_PATH = os.getenv('AIRFLOW_VAR_DATA_STAGE_HOST_PATH', DEFAULT_DATA_STAGE_HOST_PATH)

DEFAULT_SOLR_URL = "http://labcas-solr.local:8983/solr/"
DEFAULT_USERNAME = "thomas"
DEFAULT_PUBLISH_ARGS = "--collection Autoantibody_Biomarkers --steps headers hash crawl updown compare publish"

# S3 Bucket URI containing the collections to be ingested
DEFAULT_COLLECTION_ARCHIVE_BUCKET_URI="s3://edrn-labcas/archive"
DEFAULT_COLLECTION="Autoantibody_Biomarkers"

CLUSTER_NAME="publish"
TASK_ID="publish_ecs_task"
TASK_DEFINITION_NAME="labcas-publish"


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
    dag_id='ecs_ingest_dag_s3',
    description='A simple ingest DAG',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    render_template_as_native_obj=True,
    tags=['example'],
    params={
        'solr_url': SOLR_URL,
        'username': USERNAME,
        'publish_args': PUBLISH_ARGS,
        'collection_archive_bucket_s3uri': COLLECTION_ARCHIVE_BUCKET,
        'collection': COLLECTION
    },
) as dag:
    publish_task = EcsRunTaskOperator(
        task_id=TASK_ID,
        task_definition=TASK_DEFINITION_NAME,
        cluster=CLUSTER_NAME,
        launch_type="FARGATE",
        overrides={
            "containerOverrides": [
                {
                    "name": "labcas-publish", # Must match the name in the Task Definition
                    "command": "{{ params.publish_args.split() }}", # Optional: override the CMD
                    "environment": [
                        {"name": "solr", "value": "{{ params.solr_url }}"},
                        {"name": "username", "value": "{{ params.username }}"},
                        {"name": "COLLECTION_ARCHIVE_BUCKET_URI", "value": "{{ params.collection_archive_bucket_s3uri }}"},
                        {"name": "COLLECTION", "value": "{{ params.collection }}"},
                        {"name": "PUBLISH_DATA_STAGE", "value": DEFAULT_DATA_STAGE_CONTAINER_PATH}
                    ],
                },
            ],
        },
        network_configuration={
                "awsvpcConfiguration": {
                "subnets": ["subnet-0c1ea60392eb140ed", "subnet-07051748efbc8f391"],
                "securityGroups": ["sg-0972d0d74de53989b"],
                "assignPublicIp": "DISABLED", # Set to 'DISABLED' if in a private subnet with a NAT Gateway
            }
        },
        awslogs_group="/ecs/labcas-publish",
        awslogs_stream_prefix="ecs/labcas-publish",
        wait_for_completion=True
    )
    # Add more tasks or dependencies as needed
