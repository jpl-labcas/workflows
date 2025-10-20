variable "tenant" {
  description = "tenant"
  default="edrn"
}

variable "venue" {
  description = "Deployment venue (prod, test, dev)"
  default = "dev"
}

variable "operator" {
  description = "email of the person running the script"
}

variable "aws_region" {
  description = "AWS Region"
  default = "us-west-2"
}

variable "aws_profile" {
  description = "AWS profile"
  default = "default"
}

variable "ecs_task_role" {
  description = "ECS task role"
}

variable "ecs_task_execution_role" {
  description = "ECS task execution role"
}

variable "aws_fg_image" {
  description = "AWS image name for Fargate"
}

variable "aws_fg_subnets" {
  description = "AWS private subnets"
}

variable "aws_fg_vpc" {
  description = "AWS VPC"
}

