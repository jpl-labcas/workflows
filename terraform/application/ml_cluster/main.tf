locals {
  base_tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy = var.operator
  }
}

# The task definition for dask scheduler.
resource "aws_cloudwatch_log_group" "ecs_dask_scheduler" {
  name = "/ecs/labcas-${var.tenant}-${var.venue}-workflow-dask-scheduler-task"

  tags = local.base_tags
}

resource "aws_cloudwatch_log_group" "ecs_dask_worker" {
  name = "/ecs/labcas-${var.tenant}-${var.venue}-workflow-dask-scheduler-task"

  tags = local.base_tags
}

resource "aws_ecs_task_definition" "labcas-workflow-dask-ecs-scheduler-task" {
  family = "labcas-workflow-${var.tenant}-${var.venue}-dask-scheduler-task"

  container_definitions = <<EOF
  [
    {
      "name": "labcas-workflow-${var.venue}-container",
      "image": "${var.container_image}",
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
          "awslogs-group": "${aws_cloudwatch_log_group.ecs_dask_scheduler.name}",
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
      }
    }
  ]

EOF

  execution_role_arn = var.ecs_task_execution_role_arn
  task_role_arn      = var.ecs_task_role_arn

  # These are the minimum values for Fargate containers.
  cpu                      = 256
  memory                   = 512
  requires_compatibilities = ["FARGATE"]

  # This is required for Fargate containers
  network_mode = "awsvpc"

  tags = local.base_tags
}

# The task definition for dask worker.
resource "aws_ecs_task_definition" "labcas-workflow-dask-ecs-worker-task" {
  family = "labcas-workflow-${var.tenant}-${var.venue}-dask-worker-task"

  container_definitions = <<EOF
  [
    {
      "name": "labcas-workflow-${var.venue}-container",
      "image": "${var.container_image}",
      "command": [
        "worker",
        "tcp://dask-scheduler.local:8786",
        "--worker-port",
        "9000:9100"
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-region": "${var.aws_region}",
          "awslogs-group": "${aws_cloudwatch_log_group.ecs_dask_worker.name}",
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
      }
    }
  ]
EOF

  execution_role_arn = var.ecs_task_execution_role_arn
  task_role_arn      = var.ecs_task_role_arn

  # These are the minimum values for Fargate containers.
  cpu                      = 256
  memory                   = 512
  requires_compatibilities = ["FARGATE"]

  # This is required for Fargate containers
  network_mode = "awsvpc"

  tags = local.base_tags
}
