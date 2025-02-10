# LabCas Workflow

Run workflows for Labcas


## Install

### locally

Preferably use a virtual environment with python 3.9


    pip install -e '.[dev]'

### With Dask on docker

Build the docker image:

    docker build -f docker/Dockerfile . -t labcas/workflow

Start the scheduler:

    docker run -p 8787:8787 -p 8786:8786 labcas/workflow dask scheduler

Start one worker

    docker run -p 8787:8787 -p 8786:8786 labcas/workflow dask worker




    



## Run

Set you local AWS credentials to access the data


    ./aws-login.darwin.amd64


Start the dask cluster


Run the processing


    python ./src/labcas/manager/main.py

