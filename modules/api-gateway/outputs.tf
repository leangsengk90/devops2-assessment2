output "api_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.this.id
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.this.api_endpoint
}

output "api_arn" {
  description = "API Gateway ARN"
  value       = aws_apigatewayv2_api.this.arn
}

output "vpc_link_id" {
  description = "VPC Link ID"
  value       = aws_apigatewayv2_vpc_link.this.id
}

output "stage_id" {
  description = "API Gateway stage ID"
  value       = aws_apigatewayv2_stage.this.id
}

output "stage_invoke_url" {
  description = "Stage invoke URL"
  value       = aws_apigatewayv2_stage.this.invoke_url
}

output "custom_domain_name" {
  description = "Custom domain name (if configured)"
  value       = var.domain_name != null ? aws_apigatewayv2_domain_name.this[0].domain_name : null
}
