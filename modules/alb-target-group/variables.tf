variable "service_name" {
  description = "Service name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "alb_listener_arn" {
  description = "ALB listener ARN to attach the rule to"
  type        = string
}

variable "container_port" {
  description = "Port on which the container listens"
  type        = number
}

variable "listener_rule_priority" {
  description = "Priority for the listener rule (must be unique per listener)"
  type        = number
}

variable "path_patterns" {
  description = "List of path patterns to match (e.g., [\"/api1\", \"/api1/*\"])"
  type        = list(string)
}

variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/"
}

variable "health_check_protocol" {
  description = "Health check protocol"
  type        = string
  default     = "HTTP"
}

variable "health_check_matcher" {
  description = "Response codes to consider healthy"
  type        = string
  default     = "200"
}

variable "health_check_interval" {
  description = "Health check interval in seconds"
  type        = number
  default     = 30
}

variable "health_check_timeout" {
  description = "Health check timeout in seconds"
  type        = number
  default     = 5
}

variable "health_check_healthy_threshold" {
  description = "Consecutive successful health checks required"
  type        = number
  default     = 2
}

variable "health_check_unhealthy_threshold" {
  description = "Consecutive failed health checks required"
  type        = number
  default     = 3
}

variable "deregistration_delay" {
  description = "Deregistration delay in seconds"
  type        = number
  default     = 30
}
