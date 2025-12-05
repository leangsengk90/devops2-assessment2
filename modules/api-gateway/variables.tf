variable "api_name" {
  description = "Name of the API Gateway"
  type        = string
}

variable "api_description" {
  description = "Description of the API"
  type        = string
  default     = "HTTP API Gateway"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "service_name" {
  description = "Service name for tagging"
  type        = string
}

# VPC Link variables
variable "security_group_ids" {
  description = "Security group IDs for VPC Link"
  type        = list(string)
}

variable "subnet_ids" {
  description = "Subnet IDs for VPC Link"
  type        = list(string)
}

# ALB Integration
variable "alb_listener_arn" {
  description = "ARN of the ALB listener"
  type        = string
}

# Stage variables
variable "stage_name" {
  description = "API Gateway stage name"
  type        = string
  default     = "$default"
}

# Logging
variable "log_group_arn" {
  description = "CloudWatch log group ARN for access logs"
  type        = string
}

# Throttling
variable "throttle_burst_limit" {
  description = "Throttle burst limit"
  type        = number
  default     = 5000
}

variable "throttle_rate_limit" {
  description = "Throttle rate limit (requests per second)"
  type        = number
  default     = 10000
}

# CORS configuration
variable "cors_allow_origins" {
  description = "CORS allowed origins"
  type        = list(string)
  default     = ["*"]
}

variable "cors_allow_methods" {
  description = "CORS allowed methods"
  type        = list(string)
  default     = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}

variable "cors_allow_headers" {
  description = "CORS allowed headers"
  type        = list(string)
  default     = ["*"]
}

variable "cors_max_age" {
  description = "CORS max age in seconds"
  type        = number
  default     = 300
}

# Custom Domain (optional)
variable "domain_name" {
  description = "Custom domain name for API"
  type        = string
  default     = null
}

variable "certificate_arn" {
  description = "ACM certificate ARN for custom domain"
  type        = string
  default     = null
}
