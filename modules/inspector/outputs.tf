output "inspector_enabler_id" {
  description = "ID of the Inspector enabler"
  value       = var.enable_inspector ? aws_inspector2_enabler.this[0].id : null
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for Inspector findings"
  value       = var.create_sns_topic ? aws_sns_topic.inspector_findings[0].arn : null
}
