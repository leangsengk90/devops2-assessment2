# Integration with ALB via VPC Link
resource "aws_apigatewayv2_integration" "this" {
  api_id             = var.api_gateway_id
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  integration_uri    = var.alb_listener_arn
  connection_type    = "VPC_LINK"
  connection_id      = var.vpc_link_id

  request_parameters = {
    "overwrite:path" = "$request.path"
  }
}

# Route for the service (e.g., /api1/* or /auth/*)
resource "aws_apigatewayv2_route" "service_route" {
  api_id    = var.api_gateway_id
  route_key = "${var.route_prefix}/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.this.id}"
}

# Route for root path (e.g., /api1 or /auth)
resource "aws_apigatewayv2_route" "service_root" {
  api_id    = var.api_gateway_id
  route_key = var.route_prefix
  target    = "integrations/${aws_apigatewayv2_integration.this.id}"
}
