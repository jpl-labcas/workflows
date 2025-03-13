import pprint
from datetime import datetime
from datetime import timedelta
from airflow.decorators import dag
from airflow.decorators import task

from labcas.workflow.manager import process_collection
from labcas.workflow.alphan.process import process_img

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['loubrieu@jpl.nasa.gov'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'schedule_interval': None,
}


@dag(
    dag_id="nebraska",
    schedule=None,
    start_date=datetime(2021, 12, 1),
    catchup=False,
    params={
        "bucket": "edrn-bucket",
        "in_prefix": 'nebraska_images',
        "out_prefix": 'nebraska_images_nuclei',

    }
)
def taskflow(conf):
    @task(task_id="run_nebraska")
    def nebraska(**context):
        """Print the Airflow context and ds variable from the context."""
        pprint(context)
        process_collection(
            context["params"]["bucket"],
            context["params"]["in_prefix"],
            context["params"]["out_prefix"],
            process_img,
            dict(tile_size=64)
        )
        return "Whatever you return gets printed in the logs"


taskflow()




