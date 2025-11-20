variable "execution_role_arn" {
  description = "IAM role ARN for ECS task execution"
  type        = string
}

variable "task_role_arn" {
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

variable "subnet_ids" {
  description = "Subnet IDs for ECS services"
  type        = list(string)
}

variable "security_group_ids" {
  description = "Security group IDs for ECS services"
  type        = list(string)
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

variable "base_tags" {
  description = "Base tags applied to all resources"
  type        = map(string)
  default     = {
    tenant = var.tenant,
    venue = var.venue,
    application = "labcas",
    component = "workflow",
    createdBy = var.operator
  }
}
