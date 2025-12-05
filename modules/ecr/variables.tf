variable "repository_name" {
  description = "Name of the ECR repository"
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

variable "image_tag_mutability" {
  description = "Image tag mutability setting (MUTABLE or IMMUTABLE)"
  type        = string
}

variable "scan_on_push" {
  description = "Enable image scanning on push"
  type        = bool
}

variable "encryption_type" {
  description = "Encryption type (AES256 or KMS)"
  type        = string
}

variable "kms_key_arn" {
  description = "KMS key ARN for encryption (optional)"
  type        = string
}

variable "lifecycle_policy" {
  description = "ECR lifecycle policy JSON"
  type        = string
}

variable "force_delete" {
  description = "Force deletion of repository even if it contains images"
  type        = bool
}
