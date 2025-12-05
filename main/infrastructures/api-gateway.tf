# CloudWatch Log Group for API Gateway access logs
module "api_gateway_log_group" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name    = "/aws/apigateway/devops2-g4-main-${terraform.workspace}"
  retention_in_days = 7
  environment       = terraform.workspace
  service_name      = "devops2-g4-main"
}

# Shared VPC Link for all services
resource "aws_apigatewayv2_vpc_link" "main" {
  name               = "devops2-g4-vpclink-${terraform.workspace}"
  security_group_ids = [module.vpc_link_security_group.security_group_id]
  subnet_ids         = module.vpc.private_subnet_ids

  tags = {
    Name        = "devops2-g4-vpclink-${terraform.workspace}"
    Environment = terraform.workspace
    Service     = "devops2-g4-main"
  }
}

# Shared HTTP API Gateway for all services
resource "aws_apigatewayv2_api" "main" {
  name          = "devops2-g4-main-${terraform.workspace}"
  protocol_type = "HTTP"
  description   = "Main API Gateway for all microservices"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["*"]
    max_age       = 300
  }

  tags = {
    Name        = "devops2-g4-main-${terraform.workspace}"
    Environment = terraform.workspace
    Service     = "devops2-g4-main"
  }
}

# Default Stage with $default
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = module.api_gateway_log_group.log_group_arn
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
    throttling_burst_limit = 5000
    throttling_rate_limit  = 10000
  }

  tags = {
    Name        = "devops2-g4-main-stage-${terraform.workspace}"
    Environment = terraform.workspace
    Service     = "devops2-g4-main"
  }
}
