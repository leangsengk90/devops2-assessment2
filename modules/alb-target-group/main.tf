# Target Group
resource "aws_lb_target_group" "this" {
  name        = "${var.service_name}-tg-${var.environment}"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip" # For Fargate

  health_check {
    enabled             = true
    healthy_threshold   = var.health_check_healthy_threshold
    unhealthy_threshold = var.health_check_unhealthy_threshold
    timeout             = var.health_check_timeout
    interval            = var.health_check_interval
    path                = var.health_check_path
    protocol            = "HTTP"
    matcher             = var.health_check_matcher
  }

  deregistration_delay = var.deregistration_delay

  tags = {
    Name        = "${var.service_name}-tg-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Listener Rule for header-based routing
resource "aws_lb_listener_rule" "this" {
  listener_arn = var.alb_listener_arn
  priority     = var.listener_rule_priority

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }

  condition {
    http_header {
      http_header_name = "X-Service-Name"
      values           = [var.service_name]
    }
  }

  tags = {
    Name        = "${var.service_name}-listener-rule-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}
