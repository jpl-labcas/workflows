# LabCas Workflow

Run workflows for Labcas


## Install

### locally

Preferably use a virtual environment with python 3.9


    pip install -e '.[dev]'

### On ECS

Build the docker image:

    https://github.com/jpl-labcas/workflows.git



## Run

Set you local AWS credentials to access the data


    ./aws-login.darwin.amd64


Start the dask cluster


Run the processing


    python ./src/labcas/manager/main.py

