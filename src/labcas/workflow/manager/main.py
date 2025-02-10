from labcas.workflow.manager import DataStore
from labcas.workflow.steps.alphan.process import process_img

# in another terminal
# from dask.distributed import Client
# dask_client = Client(processes=False, threads_per_worker=4,
#            n_workers=1, memory_limit='2GB')
# dask_client

from distributed import Client
client = Client('127.0.0.1:8786')


def process_collection(bucket_name, in_prefix, out_prefix, fun, kwargs):
    # Use a breakpoint in the code line below to debug your script.

    datastore = DataStore(bucket_name, in_prefix, out_prefix)

    for obj in datastore.get_inputs():
        in_key = obj['Key']
        print(in_key)
        fun(
            datastore,
            in_key,
            **kwargs
        )


if __name__ == '__main__':
    process_collection(
        'edrn-bucket',
        'nebraska_images',
        'nebraska_images_nuclei',
        process_img,
        dict(tile_size=64)
    )

