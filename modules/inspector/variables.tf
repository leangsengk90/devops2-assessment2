variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "environment" {
  description = "Environment name (from terraform.workspace)"
  type        = string
}

variable "service_name" {
  description = "Service name for tagging"
  type        = string
}

variable "enable_inspector" {
  description = "Enable Amazon Inspector scanning (disable where blocked, e.g. AWS Free plan accounts)"
  type        = bool
  default     = true
}

variable "resource_types" {
  description = "Resource types to scan (Valid values: EC2, ECR, LAMBDA, LAMBDA_CODE)"
  type        = list(string)
}

variable "create_sns_topic" {
  description = "Create SNS topic for findings notifications"
  type        = bool
}

variable "notification_email" {
  description = "Email address for Inspector findings notifications (optional)"
  type        = string
}
