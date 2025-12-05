# VPC Link for API Gateway to connect to private ALB
resource "aws_apigatewayv2_vpc_link" "this" {
  name               = "${var.api_name}-vpclink-${var.environment}"
  security_group_ids = var.security_group_ids
  subnet_ids         = var.subnet_ids

  tags = {
    Name        = "${var.api_name}-vpclink-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# HTTP API Gateway
resource "aws_apigatewayv2_api" "this" {
  name          = "${var.api_name}-${var.environment}"
  protocol_type = "HTTP"
  description   = var.api_description

  cors_configuration {
    allow_origins = var.cors_allow_origins
    allow_methods = var.cors_allow_methods
    allow_headers = var.cors_allow_headers
    max_age       = var.cors_max_age
  }

  tags = {
    Name        = "${var.api_name}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Integration with ALB via VPC Link
resource "aws_apigatewayv2_integration" "alb" {
  api_id             = aws_apigatewayv2_api.this.id
  integration_type   = "HTTP_PROXY"
  integration_method = "ANY"
  integration_uri    = var.alb_listener_arn
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.this.id

  request_parameters = {
    "overwrite:path" = "$request.path"
  }
}

# Default Route (catch-all)
resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.this.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.alb.id}"
}

# Stage (deployment stage)
resource "aws_apigatewayv2_stage" "this" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = var.stage_name
  auto_deploy = true

  access_log_settings {
    destination_arn = var.log_group_arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })
  }

  default_route_settings {
    throttling_burst_limit = var.throttle_burst_limit
    throttling_rate_limit  = var.throttle_rate_limit
  }

  tags = {
    Name        = "${var.api_name}-stage-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Custom Domain (optional)
resource "aws_apigatewayv2_domain_name" "this" {
  count = var.domain_name != null ? 1 : 0

  domain_name = var.domain_name

  domain_name_configuration {
    certificate_arn = var.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  tags = {
    Name        = "${var.api_name}-domain-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# API Mapping (map custom domain to stage)
resource "aws_apigatewayv2_api_mapping" "this" {
  count = var.domain_name != null ? 1 : 0

  api_id      = aws_apigatewayv2_api.this.id
  domain_name = aws_apigatewayv2_domain_name.this[0].id
  stage       = aws_apigatewayv2_stage.this.id
}
