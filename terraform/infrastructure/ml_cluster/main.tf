# Define the cluster
resource "aws_ecs_cluster" "labcas-workflow-dask-ecs" {
  name = "labcas-${var.tenant}-${var.venue}-workflow-dask-ecs"

  tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

# Log groups hold logs from our app.
resource "aws_cloudwatch_log_group" "labcas-workflow-dask-ecs-scheduler-log-group" {
  name = "/ecs/labcas-${var.tenant}-${var.venue}-workflow-dask-scheduler-task"

  tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}



# The task definition for dask scheduler.
resource "aws_ecs_task_definition" "labcas-workflow-dask-ecs-scheduler-task" {
  family = "labcas-workflow-${var.tenant}-${var.venue}-dask-scheduler-task"

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
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

# The task definition for dask worker.
resource "aws_ecs_task_definition" "labcas-workflow-dask-ecs-worker-task" {
  family = "labcas-workflow-${var.tenant}-${var.venue}-dask-worker-task"

  container_definitions = <<EOF
  [
    {
      "name": "labcas-workflow-${var.venue}-container",
      "image": "${var.aws_fg_image}",
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
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

# a namespace for permanent dns name
resource "aws_service_discovery_private_dns_namespace" "main" {
  name        = "dask"
  description = "Private DNS Namespace for the dask ECS services"
  vpc         = var.aws_fg_vpc

  tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

resource "aws_service_discovery_service" "dask_discovery_service" {
  name = "labcas-workflow-dask-scheduler"
  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id
    dns_records {
      ttl  = 10
      type = "A"
    }
    routing_policy = "MULTIVALUE" # Or "WEIGHTED"
  }
  health_check_custom_config {
    failure_threshold = 1
  }

    tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

# The scheduler service.
resource "aws_ecs_service" "labcas-workflow-dask-ecs-scheduler-service" {
  name            = "labcas-workflow-dask-scheduler"
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
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

# auto-scaling configuration for the workers
resource "aws_appautoscaling_target" "ecs_service_target" {
  max_capacity       = 10
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.labcas-workflow-dask-ecs.name}/${aws_ecs_service.labcas-workflow-dask-ecs-worker-service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  # TODO Have an autoscaling role ?

  tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }

}

resource "aws_appautoscaling_policy" "ecs_cpu_scaling_policy" {
  name               = "ecs-cpu-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_service_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_service_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_service_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0 # Target CPU utilization percentage
    scale_in_cooldown  = 5 # seconds
    scale_out_cooldown = 5 # seconds
  }

}


# The worker service.
resource "aws_ecs_service" "labcas-workflow-dask-ecs-worker-service" {
  name            = "labcas-workflow-dask-worker"
  task_definition = aws_ecs_task_definition.labcas-workflow-dask-ecs-worker-task.arn
  cluster         = aws_ecs_cluster.labcas-workflow-dask-ecs.id
  launch_type     = "FARGATE"

  network_configuration {
    assign_public_ip = false
    security_groups = var.aws_fg_security_groups
    subnets = var.aws_fg_subnets
  }

  tags = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy : var.operator
  }
}

