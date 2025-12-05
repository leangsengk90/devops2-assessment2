variable "name" {
  description = "Name of the security group"
  type        = string
}

variable "description" {
  description = "Description of the security group"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the security group will be created"
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

variable "ingress_rules" {
  description = "List of ingress rules"
  type = list(object({
    description               = string
    from_port                 = number
    to_port                   = number
    protocol                  = string
    cidr_ipv4                 = optional(string)
    source_security_group_id  = optional(string)
  }))
  default = []
}

variable "egress_rules" {
  description = "List of egress rules"
  type = list(object({
    description                    = string
    from_port                      = number
    to_port                        = number
    protocol                       = string
    cidr_ipv4                      = optional(string)
    destination_security_group_id  = optional(string)
  }))
  default = []
}
