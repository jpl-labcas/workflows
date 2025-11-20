Installation
=============================

This section describes how to install LabCas Workflows on your system.

LabCas Workflows is meant to be installed on an Amazon Web Service account.
For development and testing purposes, you can install it on your local machine, see :doc:`develop <develop>`

Prerequisites
~~~~~~~~~~~~~~~~

What you need to install LabCas Workflows is:

* System administrator support to comply with the security constraints defined by your organization.
* An AWS account with a VPC and private subnets

Some knowledge of the AWS console and AWS CLI is helpful.


Architecture Overview
~~~~~~~~~~~~~~~~~~~~~~
The current repository is an umbrella for the 2 main components shown on the right of the following diagram:

* LabCas Workflows
* Computing resources


.. mermaid::

   graph TD
     subgraph LabCas Core
       A[UI] --> B[Backend_API]
       B --> C[(Solr_Database)]
       B --> D[(Archive_S3_bucket)]
     end
     subgraph LabCas Workflows
       F[RestFul API]
       G[Workflow_Engine_Airflow]
       H[(DAG_S3_bucket)]
       I[(Staging_S3_bucket)]
       A --> F
       F --> G
       G --> H
       G --> D
       G --> I
     end
     subgraph Computing resources
       J[Dask_Cluster_on_ECS]
       K[Other_ECS_Clusters]
       G --> J
       G --> K
     end


LabCas Core components are described there:

* `LabCas backend <https://github.com/jpl-labcas/backend>`_ (API and Solr database):
* LabCas UI: has multiple versions adapted to different projects.


Doing the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Storage Setup
-------------------------

You need 4 S3 buckets:

* Staging bucket: to store data submitted by users or created by workflows
* Archive bucket: to store data permanently, as loaded into LabCas backend
* DAG bucket: to store the workflow definitions (DAGs) and related code.
* Terraform state bucket: to store the terraform state files if you use terraform to do the installation.

You can create these buckets using the AWS console or AWS CLI.


Computing components set up
----------------------------

Depending on the workflow you want to run, you may need to set up some AWS computing components, such as:

* a Dask scalable cluster on ECS
* other ECS clusters (To Be Defined)

Dask scalable cluster on ECS
..............................

You need to create ECS cluster with Fargate launch type, and install Dask on it.

Create an **ECS cluster** with a Fargate capacity provider.

Create an **ECR registry** to store the Dask docker image.

Create the docker image locally as described in the `Integrator section <https://github.com/jpl-labcas/workflows?tab=readme-ov-file#build-the-dask-worker-image>`_ of the README file.
Push it to the ECR registry.

Create **IAM roles** and policies:

* a task role which allows to 1) read in the s3 bucket where the labcas data is, 2) write to cloudwatch
* a task execution role with the standard ECS execution policy

You will also need to create a **security group** which allows inbound communication on the port range 8786:9100 (Dask scheduler and worker ports).

Then you can create the **task definitions** for the dask scheduler and workers:

``rest Follow the terraform guidelines for the task definitions (see :doc:ecs_task_definition_terraform).

Finally, create the **ECS services** for the Dask scheduler and workers using the task definition previously created.
Optionally the ECS worker service can be set up to use auto-scaling.





Workflow engine setup
-----------------------

The workflow engine is based on Apache Airflow, running on AWS Managed Workflows for Apache Airflow (MWAA).

To Be Completed

The web API setup
-----------------------

The web API is used to trigger workflows nad edit staged metadata.

To Be Completed
