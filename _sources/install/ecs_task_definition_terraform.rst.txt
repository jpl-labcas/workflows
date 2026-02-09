Deployment of the ECS task definitions with Terraform
======================================================

You can use Terraform to deploy the ECS task definitions needed for the Dask cluster.

Prerequisites
-----------------
You need to have Terraform installed and configured with your AWS credentials.

Steps
-----------------

1. Clone the LabCas workflows repository:

   .. code-block:: bash

       git clone https://github.com/jpl-labcas/workflows.git

2. Create an environment directory from the provided template:


    .. code-block:: bash

        cp -r workflows/terraform/environments/env_template workflows/terraform/environments/your_env_name

3. Edit the `ml_cluster.tfvars` file in your new environment directory to set your AWS region, VPC ID, subnet IDs, ECS cluster name, task CPU and memory, and desired count of tasks:


   .. code-block:: text

        region           = "your-aws-region"
        vpc_id           = "your-vpc-id"
        subnet_ids       = ["subnet-id-1", "subnet-id-2"]
        ecs_cluster_name = "your-ecs-cluster-name"
        task_cpu         = "512"
        task_memory      = "1024"
        desired_count    = 2

4. Edit the `terraform.tfvars` file in the Terraform directory specify the backend configuration for storing the Terraform state.


5. Navigate to the Terraform directory for ECS task definitions:

    .. code-block:: bash

        cd workflows/terraform/application/ml_cluster

6. Initialize Terraform:

    .. code-block:: bash

        terraform init -backend-config=../../environments/your_env_name/terraform.tfvars

7. Review the Terraform plan:

    .. code-block:: bash

        terraform plan -var-file=../../environments/your_env_name/ml_cluster.tfvars

8. Apply the Terraform configuration to create the ECS task definitions:

    .. code-block:: bash

        terraform apply -var-file=../../environments/your_env_name/ml_cluster.tfvars


9. Confirm the apply action when prompted.



