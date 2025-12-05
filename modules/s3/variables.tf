
variable "bucket_name" {
  type = string
}
variable "force_destroy" {
  type = bool
}

variable "enable_public_access_block" {
  type = bool
}
variable "block_public_acls" {
  type = bool
}   
variable "block_public_policy" {
  type = bool
}
variable "ignore_public_acls" {
  type = bool
}
variable "restrict_public_buckets" {
  type = bool
}

variable "enable_versioning" {
  type = bool
}
variable "status" {
  type = string
}

variable "enable_server_side_encryption_configuration" {
  type = bool
}
variable "sse_algorithm" {
  type = string
}

variable "enable_cors_configuration" {
  type = bool
}
variable "allowed_methods" {
  type = list(string)
}
variable "allowed_origins" {
  type = list(string)
}
variable "allowed_headers" {
  type = list(string)
}
variable "max_age_seconds" {
  type = number
} 

variable "enable_lifecycle_configuration" {
  type = bool
}
variable "lifecycle_rules" {
  type = list(object({
    id                  = string
    status              = string
    prefix              = optional(string)
    noncurrent_days     = optional(number)
    expiration_days     = optional(number)
  }))
}
