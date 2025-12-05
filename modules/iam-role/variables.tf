variable "role_name" {
  description = "Name of the IAM role"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "service_name" {
  description = "Service name for tagging"
  type        = string
}

variable "assume_role_policy" {
  description = "Assume role policy JSON document"
  type        = string
}

variable "managed_policy_arns" {
  description = "List of AWS managed policy ARNs to attach"
  type        = list(string)
  default     = []
}

variable "inline_policy" {
  description = "Inline policy JSON document"
  type        = string
  default     = null
}
