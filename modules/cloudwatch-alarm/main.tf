# CloudWatch Metric Alarm
resource "aws_cloudwatch_metric_alarm" "this" {
  alarm_name          = "${var.alarm_name}-${var.environment}"
  alarm_description   = var.alarm_description
  comparison_operator = var.comparison_operator
  evaluation_periods  = var.evaluation_periods
  metric_name         = var.metric_name
  namespace           = var.namespace
  period              = var.period
  statistic           = var.statistic
  threshold           = var.threshold
  treat_missing_data  = var.treat_missing_data

  # Dimensions for ECS service metrics
  dimensions = var.dimensions

  # Actions (SNS topics, Auto Scaling policies, etc.)
  alarm_actions = var.alarm_actions
  ok_actions    = var.ok_actions

  tags = {
    Name        = "${var.alarm_name}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}
