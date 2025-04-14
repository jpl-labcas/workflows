from labcas.workflow.manager import DataStore

def process_collection(bucket_name, in_prefix, out_prefix, fun, kwargs):
    # Use a breakpoint in the code line below to debug your script.

    datastore = DataStore(bucket_name, in_prefix, out_prefix)

    for obj in datastore.get_inputs():
        in_key = obj['Key']
        print(in_key)
        print(in_key)
        fun(
            datastore,
            in_key,
            **kwargs
        )
