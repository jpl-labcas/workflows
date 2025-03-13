# LabCas Workflow

Run workflows for Labcas


## Install

### locally

Preferably use a virtual environment with python 3.9


    pip install -e '.[dev]'

### With Dask on docker

Create certificates:

    cd docker/certs
    ./generate-certs.sh

Build the docker image:

    docker build -f docker/Dockerfile . -t labcas/workflow

Start the scheduler:

    docker network create dask
    docker run --network dask -p 8787:8787 -p 8786:8786 labcas/workflow scheduler

Start one worker

    docker run  --network dask -p 8786:8786 labcas/workflow worker 


Start the client, same as in following section


### With dask on ECS

Deploy the image created in the previous section on ECR

Have a s3 bucket `labcas-infra` for the terraform state.

Other pre-requisites are:
 - a VPC
 - subnets
 - a security group allowing incoming request whre the client runs, at JPL, on EC2 or Airflow, to port 8786 and port 8787
 - a task role allowing to write on CloudWatch
 - a task execution role which pull image from ECR and standard ECS task Excecution role policy "AmazonECSTaskExecutionRolePolicy"
 

Deploy the ECS cluster with the following terraform command:

    cd terraform
    terraform init
    terraform apply \
        -var consortium="edrn" \
        -var venue="dev" \
        -var aws_fg_image=<uri of the docker image deployed on ECR>
        -var aws_fg_subnets=<private subnets of the AWS account> \
        -var aws_fg_vpc=<vpc of the AWS account> \
        -var aws_fg_security_groups  <security group> \
        -var ecs_task_role <arn of a task role>
        -var ecs_task_execution_role <arn of task execution role>




## Run

Set you local AWS credentials to access the data


    ./aws-login.darwin.amd64


Start the dask cluster


Run the processing


    python ./src/labcas/workflow/manager/main.py

