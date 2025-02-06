# LabCas Workflow

Run workflows for Labcas


## install

Preferably use a virtual environment with python 3.9


    pip install -e '.[dev]'


## Run

Set you local AWS credentials to access the data


    ./aws-login.darwin.amd64


Start the dask cluster


Run the processing


    python ./src/labcas/manager/main.py

