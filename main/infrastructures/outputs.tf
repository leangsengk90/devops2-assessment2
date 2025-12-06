# VPC Outputs
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.vpc_cidr
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

# Security Group Outputs
output "alb_security_group_id" {
  description = "ALB security group ID"
  value       = module.alb_security_group.security_group_id
}

output "ecs_security_group_id" {
  description = "ECS security group ID"
  value       = module.ecs_security_group.security_group_id
}

output "vpc_link_security_group_id" {
  description = "VPC Link security group ID"
  value       = module.vpc_link_security_group.security_group_id
}

# IAM Role Outputs
output "ecs_task_execution_role_arn" {
  description = "ECS task execution role ARN"
  value       = module.ecs_task_execution_role.role_arn
}

output "ecs_task_role_arn" {
  description = "ECS task role ARN"
  value       = module.ecs_task_role.role_arn
}

# CloudWatch Outputs
output "ecs_log_group_name" {
  description = "ECS CloudWatch log group name"
  value       = module.ecs_log_group.log_group_name
}

output "ecs_log_group_arn" {
  description = "ECS CloudWatch log group ARN"
  value       = module.ecs_log_group.log_group_arn
}

# ECR Outputs
output "ecr_api1_repository_url" {
  description = "ECR repository URL for api1"
  value       = module.ecr_api1.repository_url
}

output "ecr_api1_repository_arn" {
  description = "ECR repository ARN for api1"
  value       = module.ecr_api1.repository_arn
}

output "ecr_api1_repository_name" {
  description = "ECR repository name for api1"
  value       = module.ecr_api1.repository_name
}

# Inspector Outputs
output "inspector_sns_topic_arn" {
  description = "SNS topic ARN for Inspector findings"
  value       = module.inspector.sns_topic_arn
}

# API Gateway Outputs
output "api_gateway_id" {
  description = "Main API Gateway ID"
  value       = aws_apigatewayv2_api.main.id
}

output "api_gateway_endpoint" {
  description = "Main API Gateway endpoint"
  value       = aws_apigatewayv2_api.main.api_endpoint
}

output "api_gateway_execution_arn" {
  description = "Main API Gateway execution ARN"
  value       = aws_apigatewayv2_api.main.execution_arn
}

output "vpc_link_id" {
  description = "VPC Link ID for API Gateway"
  value       = aws_apigatewayv2_vpc_link.main.id
}

output "ecr_auth_repository_url" {
  description = "ECR repository URL for auth"
  value       = module.ecr_auth.repository_url
}

output "ecr_auth_repository_arn" {
  description = "ECR repository ARN for auth"
  value       = module.ecr_auth.repository_arn
}

output "ecr_auth_repository_name" {
  description = "ECR repository name for auth"
  value       = module.ecr_auth.repository_name
}

output "ecr_profile_repository_url" {
  description = "ECR repository URL for profile"
  value       = module.ecr_profile.repository_url
}

output "ecr_profile_repository_arn" {
  description = "ECR repository ARN for profile"
  value       = module.ecr_profile.repository_arn
}

output "ecr_profile_repository_name" {
  description = "ECR repository name for profile"
  value       = module.ecr_profile.repository_name
}

output "ecr_messenger_repository_url" {
  description = "ECR repository URL for messenger"
  value       = module.ecr_messenger.repository_url
}

output "ecr_messenger_repository_arn" {
  description = "ECR repository ARN for messenger"
  value       = module.ecr_messenger.repository_arn
}

output "ecr_messenger_repository_name" {
  description = "ECR repository name for messenger"
  value       = module.ecr_messenger.repository_name
}

output "ecr_finance_repository_url" {
  description = "ECR repository URL for finance"
  value       = module.ecr_finance.repository_url
}

output "ecr_finance_repository_arn" {
  description = "ECR repository ARN for finance"
  value       = module.ecr_finance.repository_arn
}

output "ecr_finance_repository_name" {
  description = "ECR repository name for finance"
  value       = module.ecr_finance.repository_name
}

output "ecr_share_repository_url" {
  description = "ECR repository URL for share"
  value       = module.ecr_share.repository_url
}

output "ecr_share_repository_arn" {
  description = "ECR repository ARN for share"
  value       = module.ecr_share.repository_arn
}

output "ecr_share_repository_name" {
  description = "ECR repository name for share"
  value       = module.ecr_share.repository_name
}
