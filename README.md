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


Start the client, same as in following section


### With dask on ECS

Deploy the image created in the previous section on ECR

Have a s3 bucket `labcas-infra` for the terraform state.

Deploy the ECS cluster with the following terraform command:

    cd terraform
    terraform init
    terraform apply \
        -var consortium="edrn" \
        -var venue="dev" \
        -var aws_fg_subnets=<private subnets of the AWS account> \
        -var aws_fg_vpc=<vpc of the AWS account> \
        -var aws_fg_security_groups  <security group allows incoming request whre the client runs, at JPL, on EC@ or Airflow, to port 8786 and port 8787> \
        -var ecs_task_role <arn of a role allowing to write on cloudwatch>
        -var ecs_task_execution_role <arn of role which can pull image from ECR and standard ECS task Excecution role policy "AmazonECSTaskExecutionRolePolicy">




## Run

Set you local AWS credentials to access the data


    ./aws-login.darwin.amd64


Start the dask cluster


Run the processing


    python ./src/labcas/manager/main.py

