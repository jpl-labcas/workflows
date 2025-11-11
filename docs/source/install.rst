Installation
=============================

This section describes how to install LabCas Workflows on your system.

LabCas Workflows is meant to be installed on an Amazon Web Service account.
For development and testing purposes, you can install it on your local machine, see :doc:`develop <develop>`

Prerequisites
~~~~~~~~~~~~~~~~

What you need to install LabCas Workflows is:

* An AWS account

Some knowledge of the AWS console and AWS CLI is helpful.


Architecture Overview
~~~~~~~~~~~~~~~~~~~~~~

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












Doing the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




Storage Setup
-------------------------

You need 3 S3 buckets:
- Staging bucket: to store data submited or created by workflows
- Archive bucket: to store data permanently, as loaded into LabCas backend
- DAG bucket: to store the workflow definitions (DAGs) and related code.

You can create these buckets using the AWS console or AWS CLI.

Computing components set up
----------------------------

Depending on the workflow you want to run, you may need to set up some AWS computing components, such as:

* a Dask scalable cluster on ECS
* other ECS clusters (To Be Defined)

Dask scalable cluster on ECS
..............................

To Be Completed


Workflow engine setup
-----------------------

The workflow engine is based on Apache Airflow, running on AWS Managed Workflows for Apache Airflow (MWAA).


The web API setup
-----------------------

The web API is used to trigger workflows nad edit staged metadata
