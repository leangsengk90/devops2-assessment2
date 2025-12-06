# Shared Application Load Balancer for all services
resource "aws_lb" "shared" {
  name               = "devops2-g4-shared-alb-${terraform.workspace}"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [module.alb_security_group.security_group_id]
  subnets            = module.vpc.private_subnet_ids

  enable_deletion_protection = false
  enable_http2              = true

  tags = {
    Name        = "devops2-g4-shared-alb-${terraform.workspace}"
    Environment = terraform.workspace
    Service     = "devops2-g4-shared"
  }
}

# HTTP Listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.shared.arn
  port              = 80
  protocol          = "HTTP"

  # Default action - return 404
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Service not found"
      status_code  = "404"
    }
  }

  tags = {
    Name        = "devops2-g4-shared-http-listener-${terraform.workspace}"
    Environment = terraform.workspace
    Service     = "devops2-g4-shared"
  }
}
