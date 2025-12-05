# ALB Outputs
output "alb_dns_name" {
  description = "ALB DNS name"
  value       = module.alb.alb_dns_name
}

output "target_group_arn" {
  description = "Target group ARN"
  value       = module.alb.target_group_arn
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
  description = "API Gateway invoke URL for auth"
  value       = "${data.terraform_remote_state.infrastructure.outputs.api_gateway_endpoint}/auth"
}

output "integration_id" {
  description = "API Gateway integration ID"
  value       = module.api_gateway_route.integration_id
}
