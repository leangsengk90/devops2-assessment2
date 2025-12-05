variable "api_gateway_id" {
  description = "API Gateway ID"
  type        = string
}

variable "vpc_link_id" {
  description = "VPC Link ID"
  type        = string
}

variable "alb_listener_arn" {
  description = "ALB listener ARN for integration"
  type        = string
}

variable "route_prefix" {
  description = "Route prefix (e.g., /api1, /auth)"
  type        = string
}

variable "service_name" {
  description = "Service name for tagging"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}
