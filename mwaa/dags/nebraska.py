from airflow.decorators import dag
from airflow.decorators import task
from airflow.models import DagRun
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from distributed import Client

from labcas.workflow.manager import process_collection
from labcas.workflow.steps.alphan.process import process_img

## local test tcp://dask-scheduler:8786
## on AWS 100.65.218.187
#DASK_SCHEDULER = "tcp://100.65.218.186:8786"
DASK_SCHEDULER = "tcp://dask-scheduler.local:8786"
IN_BUCKET_PARAM = Param(
        default="edrn-bucket",
        description="S3 bucket where the input data are found",
        type="string"
)

IN_PREFIX_PARAM =  Param(
        default='nebraska_images/',
        description="S3 bucket prefix (path) where the input data are found",
        type="string"
)

OUT_BUCKET_PARAM = Param(
        default="edrn-bucket",
        description="S3 bucket where the output data is going to be written",
        type="string"
)

OUT_PREFIX_PARAM = Param(
        default="nebraska_images_nuclei",
        description="S3 bucket prefix (path) where the output data is going to be written",
        type="string"
)

TILE_SIZE_PARAM = Param(
        default=64,
        description="Tile size, option available are 64, 128, 256",
        type="integer"
)

CSV_PARAM = Param(
        default=True,
        description="True is we wnt to produce a CSV with the nuclei statistics, False otherwise",
        type="boolean"
)

default_args = {
    "in_bucket": IN_BUCKET_PARAM,
    "in_prefix": IN_PREFIX_PARAM,
    "out_bucket": OUT_BUCKET_PARAM,
    "out_prefix": OUT_PREFIX_PARAM,
    "tile_size": 64,
    "csv": True
}


@dag(
    dag_id="nebraska",
    description="EDRN workflow detecting cells nuclei on image with machine learning technologies",
    doc_md="something to start with",
    params=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['EDRN']
)
def nebraska_dag():

    @task()
    def nebraska_task(dag_run: DagRun):
        """Print the Airflow context and ds variable from the context."""

        tile_size = dag_run.conf.get('tile_size', 64)
        csv = dag_run.conf.get('csv', True)
        in_bucket = dag_run.conf.get('in_bucket')
        in_prefix = dag_run.conf.get('in_prefix')
        out_bucket = dag_run.conf.get('out_bucket')
        out_prefix = dag_run.conf.get('out_prefix')

        print(f"Run nebraska use case on dask {DASK_SCHEDULER}")
        print(f"Using input files on s3://{in_bucket}/{in_prefix}")
        print(f"Writing putput files to s3://{out_bucket}/{out_prefix}")
        client = Client(DASK_SCHEDULER)
        # TODO enable to write result in different bucket
        process_collection(in_bucket, in_prefix, out_bucket, out_prefix, process_img, dict(tile_size=tile_size, csv=csv))
        return "Whatever you return gets printed in the logs"

    result = nebraska_task()


nebraska_dag = nebraska_dag()








