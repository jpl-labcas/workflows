# Define the cluster
resource "aws_ecs_cluster" "labcas-workflow-dask-ecs" {
  name = "labcas-${var.consortium}-${var.venue}-workflow-dask-ecs"

  tags = {
    application = "labcas"
    component = "workflow"
    consortium = var.consortium
    venue = var.venue
  }
}

# Log groups hold logs from our app.
resource "aws_cloudwatch_log_group" "labcas-workflow-dask-ecs-scheduler-log-group" {
  name = "/ecs/labcas-${var.consortium}-${var.venue}-workflow-dask-scheduler-task"

  tags = {
    application = "labcas"
    component = "workflow"
    service = "scheduler"
    consortium = var.consortium
    venue = var.venue
  }
}

# Log groups hold logs from our app.
resource "aws_cloudwatch_log_group" "labcas-workflow-dask-ecs-worker-log-group" {
  name = "/ecs/labcas-${var.consortium}-${var.venue}-workflow-dask-worker-task"

  tags = {
    application = "labcas"
    component = "workflow"
    service = "scheduler"
    consortium = var.consortium
    venue = var.venue
  }
}


# The task definition for dask scheduler.
resource "aws_ecs_task_definition" "labcas-workflow-dask-ecs-scheduler-task" {
  family = "labcas-workflow-${var.consortium}-${var.venue}-dask-scheduler-task"

  container_definitions = <<EOF
  [
    {
      "name": "labcas-workflow-${var.venue}-container",
      "image": "${var.aws_fg_image}",
      "portMappings": [
        {
          "containerPort": 8786,
          "protocol": "tcp"
        },
        {
          "containerPort": 8787
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-region": "${var.aws_region}",
          "awslogs-group": "${aws_cloudwatch_log_group.labcas-workflow-dask-ecs-scheduler-log-group}",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck" : {
        "retries": 3,
        "command": [
          "CMD-SHELL",
          "date || exit 1"
        ],
        "timeout": 5,
        "interval": 60,
        "startPeriod": 300
      },
    }
  ]

EOF

  execution_role_arn = var.ecs_task_execution_role
  task_role_arn      = var.ecs_task_role

  # These are the minimum values for Fargate containers.
  cpu                      = 256
  memory                   = 512
  requires_compatibilities = ["FARGATE"]

  # This is required for Fargate containers
  network_mode = "awsvpc"

  tags = {
    application = "labcas"
    component = "workflow"
    service = "scheduler"
    consortium = var.consortium
    venue = var.venue
  }
}


# The task definition for dask worker.
resource "aws_ecs_task_definition" "labcas-workflow-dask-ecs-worker-task" {
  family = "labcas-workflow-${var.consortium}-${var.venue}-dask-worker-task"

  container_definitions = <<EOF
  [
    {
      "name": "labcas-workflow-${var.venue}-container",
      "image": "${var.aws_fg_image}",
      "command": "worker",
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-region": "${var.aws_region}",
          "awslogs-group": "${aws_cloudwatch_log_group.labcas-workflow-dask-ecs-worker-log-group}",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck" : {
        "retries": 3,
        "command": [
          "CMD-SHELL",
          "date || exit 1"
        ],
        "timeout": 5,
        "interval": 60,
        "startPeriod": 300
      },
    }
  ]

EOF

  execution_role_arn = var.ecs_task_execution_role
  task_role_arn      = var.ecs_task_role

  # These are the minimum values for Fargate containers.
  cpu                      = 256
  memory                   = 512
  requires_compatibilities = ["FARGATE"]

  # This is required for Fargate containers
  network_mode = "awsvpc"

  tags = {
    application = "labcas"
    component = "workflow"
    service = "scheduler"
    consortium = var.consortium
    venue = var.venue
  }
}



# The scheduler service.
resource "aws_ecs_service" "labcas-workflow-dask-ecs-scheduler-service" {
  name            = "labcas-workflow-${var.consortium}-${var.venue}-dask-ecs-scheduler-service"
  task_definition = aws_ecs_task_definition.labcas-workflow-dask-ecs-scheduler-task.arn
  cluster         = aws_ecs_cluster.labcas-workflow-dask-ecs.id
  launch_type     = "FARGATE"

  desired_count = 1

  network_configuration {
    assign_public_ip = false
    security_groups = var.aws_fg_security_groups
    subnets = var.aws_fg_subnets
  }

  tags = {
    application = "labcas"
    component = "workflow"
    service = "scheduler"
    consortium = var.consortium
    venue = var.venue
  }
}

# The worker service.
resource "aws_ecs_service" "labcas-workflow-dask-ecs-worker-service" {
  name            = "labcas-workflow-${var.consortium}-${var.venue}-dask-ecs-worker-service"
  task_definition = aws_ecs_task_definition.labcas-workflow-dask-ecs-worker-task.arn
  cluster         = aws_ecs_cluster.labcas-workflow-dask-ecs.id
  launch_type     = "FARGATE"

  desired_count = 3

  network_configuration {
    assign_public_ip = false
    security_groups = var.aws_fg_security_groups
    subnets = var.aws_fg_subnets
  }

  tags = {
    application = "labcas"
    component = "workflow"
    service = "scheduler"
    consortium = var.consortium
    venue = var.venue
  }
}

