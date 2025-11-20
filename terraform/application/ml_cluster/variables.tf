variable "aws_profile" {
  description = "AWS CLI profile to use for authentication"
  type        = string
}

variable "ecs_task_execution_role_arn" {
  description = "IAM role ARN for ECS task execution"
  type        = string
}

variable "ecs_task_role_arn" {
  description = "IAM role ARN assumed by the task"
  type        = string
}

variable "container_image" {
  description = "Full container image reference (e.g., <acct>.dkr.ecr.<region>.amazonaws.com/repo:tag)"
  type        = string
}

variable "aws_region" {
  description = "AWS region for logs and account-specific settings"
  type        = string
}

variable "tenant" {
  description = "Tenant identifier"
  type        = string
  default     = ""
}

variable "venue" {
  description = "Venue identifier"
  type        = string
  default     = ""
}

variable "operator" {
  description = "Person who created the resources"
  type        = string
  default     = ""
}


