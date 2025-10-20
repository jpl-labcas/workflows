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


## Deployment

### Terraform initialization

    cd terraform
    terraform init
 
### Create or update the storage

We need S3 bucket to manage the storage:

    cd terraform/buckets
    terraform apply

### Create or update the Machine Learning Cluster

    cd terraform/ml_cluster
    terraform apply


### Create the workflow engine

TBD


### Create the workflow API

TBD



