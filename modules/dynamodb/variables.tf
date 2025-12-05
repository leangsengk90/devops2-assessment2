variable "dynamodb_table_name" {
  type = string
}

variable "billing_mode" {
  type    = string
}

variable "hash_key" {
    type = string
}

variable "hash_key_type" {
    type = string
}

variable "ttl_attribute_name" {
    type = string
}

variable "ttl_enabled" {
    type = bool
}

variable "server_side_encryption_enabled" {
    type = bool
}

