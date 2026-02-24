# LabCas Workflow

Run workflows for Labcas

Depending on what you do, there are multiple ways of running a labcase workflow:

- **Developers:** for developers: local run, natively running on your OS
- **Integrators:** for AWS Managed Apache Airflow integrators (mwaa), with a local mwaa
- **System Administrators:** for System administors, deployed/configured on AWS
- **End users:** For end users, using the AWS deployment.


## Developers

To run tasks locally, independently from the workflow engine, AirFlow.

### Install

With python 3.11, preferably use a virtual environment


    pip install -e '.[dev]'

### Set AWS connection

    ./aws-login.darwin.amd64
    export AWS_PROFILE=saml-pub

### Run/Test the client

#### Without a dask cluster:

    python src/labcas/workflow/manager/main.py


#### With a local dask cluster

Start the scheduler:

    docker network create dask
    docker run --network dask -p 8787:8787 -p 8786:8786 labcas/workflow scheduler

Start one worker

    docker run  --network dask -p 8786:8786 labcas/workflow worker 


Start the client, same as in previous section but add the `tcp://localhost:8787` argument to the dask client in the `main.py` script 



### Deploy package on pypi

Upgrade the version in file "src/labcas/workflow/VERSION.txt"

Publish the package on pypi:

    pip install build
    pip install twine
    rm dist/*
    python -m build
    twine upload dist/*

### Update documentation

The documentation is built with Sphinx.

The sources are in the `docs/source` directory.

To built the documentation locally, run:

    sphinx-build -b html docs site  

The documentation can be viewed in the browser at `site/index.html`.

Publish the documentation by pushing the source updates to the `main` branch. A github action will build and publish the documentation.

The documentation is publicly hosted on [LabCas Workflow documentation](https://jpl-labcas.github.io/workflows/)




## Integrators

### Build the Dask worker image

Update the labcas.workflow dependency version as needed in `docker/Dockerfile`, then:

    docker build -f docker/Dockerfile . -t labcas/workflow

### Create a managed AirFlow docker image to be run locally

#### Authorize the MWAA to launch local docker containers

Mandatory if you use the DockerOperator, as done in the ingest DAG.

On you lcoal host, get the group for you docker socket interface:

    ls -l /var/run/docker.sock 
    lrwxr-xr-x  1 root  daemon  39 Nov 19 15:52 /var/run/docker.sock -> /Users/loubrieu/.docker/run/docker.sock

    ls -l /Users/loubrieu/.docker/run/docker.sock
    srw-rw----  1 loubrieu  staff  0 Nov ...

Here the group we are interested in is `staff`.

Get the group id (on MacOS)

    dscl . -read /Groups/staff PrimaryGroupID
    PrimaryGroupID: 20

Add that group id in the docker-compose-local.yml file, in the section:

    local-runner:
      image: amazon/mwaa-local:2_10_3
      group_add:
        - 20  # docker group id to enable docker-in-docker
      ...

Then in the `aws-mwaa-local-runner` repository, update the docker file in `docker/Dockerfile` to add the airflow user to that group:

    RUN groupdel games && groupadd -g 20 staff && usermod -aG staff airflow

(in this case, it was also necessary to delete the existing group `games` with gid 20).

Also, at last, and that might be enough, but I did not test that without the previous configuration:
In the `docker/scripts/entrypoint.sh` file, add the following line:

    chmod 666 /var/run/docker.sock

#### Create the MWAA local image

Use repository https://github.com/aws/aws-mwaa-local-runner, clone it, then:

    ./mwaa-local-env build-image

Then from your local labcas_workflow repository:

    cd mwaa

As needed, update requirements in `requirements` directory and dags in `dags` directory.

### Update the AWS credentials

Optionally, needed if your DAG reads/writes from/to AWS S3 or other AWS services.

    aws-login.darwin.amd64
    cp -r ~/.aws .
    eval $(aws configure export-credentials --profile saml-pub --format env)





### Prepare/Update the solr configuration (optional)

Clone the labcas-backend repository if not already done:

    git clone https://github.com/jpl-labcas/backend
    
Set your labcas home in a temporary directory:

    export LABCAS_HOME=/tmp/labcas


Build it (you need jdk8 and compatible maven):

    cd backend
    mvn clean install

Copy the solr generated configuration in our local docker compose environment:

    cp -r /tmp/labcas/solr-home ./solr/confs/

### Configure Environment Variables

The following environment variables will need to be set in order for certain DAGs to function

- `LABCAS_LOCAL_DATA_LAKE`
  - Path to Local Directory acting as the Ingest Data Lake
- `LABCAS_LOCAL_DATA_STAGE`
  - Path to Local Directory acting as the Ingest Data Stage

### Launch the services


Create the network before, so that it can be accessed from within the mwaa local runner:

    docker network create labcas

Launch the services (solr, mwaa local runner, dask services):
 
    docker compose -f docker-compose-local.yml up

Test the server on http://localhost:8080 , login admin/test

### Stop 

    Ctrl^C

### Stop and re-initialize local volumes

    docker compose  -f ./docker-compose-local.yml down -v

    

See the console on http://localhost:8080, admin/test

### Test the requirements.txt files

In the `aws-mwaa-local-runner` repository, run
 
    ./mwaa-local-env test-requirements

This will test the requirements.txt files in the `requirements` directory.

### Debug the workflow import

(docker compose should be running)

    docker container ls

Pick the container id of image "amazon/mwaa-local:2_10_3", for example '54706271b7fc':

Then open a bash interpreter in the docker container:

    docker exec -it 54706271b7fc bash

And, in the bash prompt:

    cd dags
    python3 -c "import nebraska"


## System administrators

The deployment requires:
- one ECS cluster for the dask cluster.
- Optionally, an EC2 instance client of the Dask cluster
- One managed Airflow

### dask on ECS

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

### Test the dask cluster

#### Connect to an EC2 instance, client of the Dask cluster


    ssh {ip of the EC2 instance}
    aws-login
    export AWS_PROFILE=saml-pub
    git clone {this repository}
    cd workflows
    source venv/bin/activate
    python src/labcas/workflow/manager/main.py


To See Dask Dashboard, open SSH tunnels:

    ssh -L 8787:{dask scheduler ip on ECS}:8787 {username}@{ec2 instance ip}
    ssh -L 8787:{dask scheduler ip on ECS}:8787 {username}@{ec2 instance ip}

in browser: http://localhost:8787


### Apache Airflow

An AWS managed Airflow is deployed in version 2.10.3.

The managed Airflow is authorized to read and write in the data bucket.

The managed Airflow is authorized to access the ECS security group.

It uses s3 bucket {labcas_airflow}.

Upload to S3 the `./mwaa/requirements/requirements.txt` file to the bucket in: `s3:/{labas_airflow}/requirements/`

Upload to S3 the `./mwaa/dags/nebraska.py` file to the bucket in: `s3:/{labas_airflow}/dags/`

Update the version of the `requirements.txt` file in the Airflow configuration console.

Test, go the the Airflow web console, and trigger the nebraska dag.
