output "target_group_arn" {
  description = "Target group ARN"
  value       = aws_lb_target_group.this.arn
}

output "target_group_name" {
  description = "Target group name"
  value       = aws_lb_target_group.this.name
}

output "listener_rule_arn" {
  description = "Listener rule ARN"
  value       = aws_lb_listener_rule.this.arn
}
