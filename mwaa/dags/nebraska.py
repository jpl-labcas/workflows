from airflow.decorators import dag
from airflow.decorators import task
from airflow.utils.dates import days_ago
from distributed import Client

from labcas.workflow.manager import process_collection
from labcas.workflow.steps.alphan.process import process_img

default_args = {
    "dask_scheduler": "tcp://dask-scheduler:8786",
    "bucket": "edrn-bucket",
    "in_prefix": 'nebraska_images',
    "out_prefix": 'nebraska_images_nuclei',
}


@dag(dag_id="nebraska", default_args=default_args, schedule_interval="@daily", start_date=days_ago(1), tags=['EDRN'])
def nebraska_dag():

    @task()
    def nebraska_task(dask_scheduler: str, bucket :str, in_prefix: str, out_prefix: str):
        """Print the Airflow context and ds variable from the context."""
        client = Client(dask_scheduler)
        process_collection(bucket, in_prefix, out_prefix, process_img, dict(tile_size=64))
        print("whatever")
        return "Whatever you return gets printed in the logs"

    result = nebraska_task(
            dask_scheduler = default_args["dask_scheduler"],
            bucket = default_args["bucket"],
            in_prefix = default_args["in_prefix"],
            out_prefix = default_args["out_prefix"]
    )
    result = nebraska_task()


nebraska_dag = nebraska_dag()








