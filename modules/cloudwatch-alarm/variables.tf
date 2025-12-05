variable "alarm_name" {
  description = "Name of the CloudWatch alarm"
  type        = string
}

variable "alarm_description" {
  description = "Description of the alarm"
  type        = string
}

variable "comparison_operator" {
  description = "Arithmetic operation to use when comparing statistic and threshold"
  type        = string
}

variable "evaluation_periods" {
  description = "Number of periods over which data is compared to threshold"
  type        = number
}

variable "metric_name" {
  description = "Name of the metric"
  type        = string
}

variable "namespace" {
  description = "Namespace for the metric"
  type        = string
}

variable "period" {
  description = "Period in seconds over which statistic is applied"
  type        = number
}

variable "statistic" {
  description = "Statistic to apply to the metric"
  type        = string
}

variable "threshold" {
  description = "Threshold value to compare metric against"
  type        = number
}

variable "treat_missing_data" {
  description = "How to treat missing data"
  type        = string
  default     = "notBreaching"
}

variable "dimensions" {
  description = "Dimensions for the metric"
  type        = map(string)
  default     = {}
}

variable "alarm_actions" {
  description = "List of ARNs to notify when alarm transitions to ALARM state"
  type        = list(string)
  default     = []
}

variable "ok_actions" {
  description = "List of ARNs to notify when alarm transitions to OK state"
  type        = list(string)
  default     = []
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "service_name" {
  description = "Service name for tagging"
  type        = string
}
