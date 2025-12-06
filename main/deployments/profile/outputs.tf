# ALB Outputs
output "alb_dns_name" {
  description = "ALB DNS name"
  value       = data.terraform_remote_state.infrastructure.outputs.shared_alb_dns_name
}

output "target_group_arn" {
  description = "Target group ARN"
  value       = module.alb_target_group.target_group_arn
}

# ECS Outputs
output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = module.ecs_cluster.cluster_name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = module.ecs_service.service_name
}

# API Gateway Outputs
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = data.terraform_remote_state.infrastructure.outputs.api_gateway_endpoint
}

output "api_invoke_url" {
  description = "API Gateway invoke URL for profile"
  value       = "${data.terraform_remote_state.infrastructure.outputs.api_gateway_endpoint}/profile"
}

output "integration_id" {
  description = "API Gateway integration ID"
  value       = module.api_gateway_route.integration_id
}
