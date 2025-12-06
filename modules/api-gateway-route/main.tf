# Integration with ALB via VPC Link
resource "aws_apigatewayv2_integration" "this" {
  api_id             = var.api_gateway_id
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  integration_uri    = var.alb_listener_arn
  connection_type    = "VPC_LINK"
  connection_id      = var.vpc_link_id

  # Strip the service prefix and add custom header for ALB routing
  # /finance/api/hello -> /api/hello (with X-Service-Name: finance header)
  request_parameters = {
    "overwrite:path"                = "/$request.path.proxy"
    "append:header.X-Service-Name"  = var.service_name
  }
}

# Route for the service with path variable (e.g., ANY /api1/{proxy+})
resource "aws_apigatewayv2_route" "service_route" {
  api_id    = var.api_gateway_id
  route_key = "ANY ${var.route_prefix}/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.this.id}"
}

# Integration for root path (without proxy variable)
resource "aws_apigatewayv2_integration" "root" {
  api_id             = var.api_gateway_id
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  integration_uri    = var.alb_listener_arn
  connection_type    = "VPC_LINK"
  connection_id      = var.vpc_link_id

  # Root path: /finance -> / (with X-Service-Name header)
  request_parameters = {
    "overwrite:path"                = "/"
    "append:header.X-Service-Name"  = var.service_name
  }
}

# Route for root path (e.g., ANY /api1)
resource "aws_apigatewayv2_route" "service_root" {
  api_id    = var.api_gateway_id
  route_key = "ANY ${var.route_prefix}"
  target    = "integrations/${aws_apigatewayv2_integration.root.id}"
}
