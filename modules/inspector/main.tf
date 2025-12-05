resource "aws_inspector2_enabler" "this" {
  account_ids    = [var.account_id]
  resource_types = var.resource_types

  timeouts {
    create = "15m"
    update = "15m"
    delete = "15m"
  }
}

# Optional: Create an SNS topic for Inspector findings
resource "aws_sns_topic" "inspector_findings" {
  count = var.create_sns_topic ? 1 : 0
  name  = "${var.service_name}-inspector-findings-${var.environment}"

  tags = {
    Name        = "${var.service_name}-inspector-findings-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
    ManagedBy   = "terraform"
  }
}

resource "aws_sns_topic_subscription" "inspector_email" {
  count     = var.create_sns_topic && var.notification_email != null ? 1 : 0
  topic_arn = aws_sns_topic.inspector_findings[0].arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# EventBridge rule to capture Inspector findings
resource "aws_cloudwatch_event_rule" "inspector_findings" {
  count       = var.create_sns_topic ? 1 : 0
  name        = "${var.service_name}-inspector-findings-${var.environment}"
  description = "Capture Inspector findings"

  event_pattern = jsonencode({
    source      = ["aws.inspector2"]
    detail-type = ["Inspector2 Finding"]
  })

  tags = {
    Name        = "${var.service_name}-inspector-findings-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
    ManagedBy   = "terraform"
  }
}

resource "aws_cloudwatch_event_target" "inspector_sns" {
  count     = var.create_sns_topic ? 1 : 0
  rule      = aws_cloudwatch_event_rule.inspector_findings[0].name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.inspector_findings[0].arn
}

resource "aws_sns_topic_policy" "inspector_findings" {
  count  = var.create_sns_topic ? 1 : 0
  arn    = aws_sns_topic.inspector_findings[0].arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.inspector_findings[0].arn
      }
    ]
  })
}
