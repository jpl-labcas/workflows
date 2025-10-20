# Deployment of the workflow framework with terraform

## Prerequisites

### On AWS

- an account
- a VPC
- private subnets
- a task role which allows to 1) read in the s3 bucket where the labcas data is, 2) write to cloudwatch
- a task execution role with the standard ECS execution policy
- a security group with inbound authorization on port range 8786:9100
- the docker image from this project deployed on ECR

### For your configuration 

- a tenant (ERDN or JPL_NIST or NIST)
- a venue (dev or prod)
- a terraform backend s3 bucket, e.g. `jpl_nist-prod-labcas-admin`, update file provider.tf with your value. This is used to save the terraform states.

You can create a var file with a content like:

    aws_region="us-west-1"
    aws_profile="my-profile"
    tenant="nist_jpl"
    venue="dev"
    operator="john.doe@gmail.com"
    aws_fg_image="TBD"
    ecs_task_execution_role="TBD"
    ecs_task_role="TBD"
    aws_fg_security_groups="TBD"
    aws_fg_subnets="TBD"
    aws_fg_vpc="TBD"


## Deployment

### Terraform initialization

    cd terraform
    terraform init
 
### Create or update the storage

We need S3 bucket to manage the storage:

    cd terraform/buckets
    terraform apply -var-file my_variables.tf

### Create or update the Machine Learning Cluster

    cd terraform/ml_cluster
    terraform apply -var-file my_variables.tf


### Create the workflow engine

TBD


### Create the workflow API

TBD



