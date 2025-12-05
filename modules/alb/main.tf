# Application Load Balancer
resource "aws_lb" "this" {
  name               = "${var.name}-${var.environment}"
  internal           = var.internal
  load_balancer_type = "application"
  security_groups    = var.security_group_ids
  subnets            = var.subnet_ids

  enable_deletion_protection = var.enable_deletion_protection
  enable_http2              = var.enable_http2

  tags = {
    Name        = "${var.name}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Target Group
resource "aws_lb_target_group" "this" {
  name        = "${var.name}-tg-${var.environment}"
  port        = var.target_group_port
  protocol    = var.target_group_protocol
  vpc_id      = var.vpc_id
  target_type = "ip" # For Fargate

  health_check {
    enabled             = true
    healthy_threshold   = var.health_check_healthy_threshold
    unhealthy_threshold = var.health_check_unhealthy_threshold
    timeout             = var.health_check_timeout
    interval            = var.health_check_interval
    path                = var.health_check_path
    protocol            = var.health_check_protocol
    matcher             = var.health_check_matcher
  }

  deregistration_delay = var.deregistration_delay

  tags = {
    Name        = "${var.name}-tg-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# HTTP Listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }

  tags = {
    Name        = "${var.name}-http-listener-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# HTTPS Listener (optional - if certificate ARN provided)
resource "aws_lb_listener" "https" {
  count = var.certificate_arn != null ? 1 : 0

  load_balancer_arn = aws_lb.this.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = var.ssl_policy
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }

  tags = {
    Name        = "${var.name}-https-listener-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}
