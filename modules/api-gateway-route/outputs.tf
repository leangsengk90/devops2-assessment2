output "integration_id" {
  description = "API Gateway integration ID"
  value       = aws_apigatewayv2_integration.this.id
}

output "route_id" {
  description = "API Gateway route ID"
  value       = aws_apigatewayv2_route.service_route.id
}

output "root_route_id" {
  description = "API Gateway root route ID"
  value       = aws_apigatewayv2_route.service_root.id
}
