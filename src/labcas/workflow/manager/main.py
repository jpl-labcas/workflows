import os
from labcas.workflow.manager import DataStore
from labcas.workflow.steps.alphan.process import process_img
from distributed import Client
from distributed.security import Security

sec = Security(
    tls_ca_file=os.getenv("DASK_TLS_CA"),
    tls_client_cert=os.getenv("DASK_TLS_CERT"),
    tls_client_key=os.getenv("DASK_TLS_KEY"),
    require_encryption=True
)

client = Client('tls://127.0.0.1:8786')


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

