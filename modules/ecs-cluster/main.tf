# ECS Cluster
resource "aws_ecs_cluster" "this" {
  name = "${var.cluster_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = var.enable_container_insights ? "enabled" : "disabled"
  }

  tags = {
    Name        = "${var.cluster_name}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# CloudWatch Log Group for Container Insights (if enabled)
# Note: ECS creates this automatically when Container Insights is enabled
# We use data source to reference it instead of creating it
data "aws_cloudwatch_log_group" "container_insights" {
  count = var.enable_container_insights ? 1 : 0
  name  = "/aws/ecs/containerinsights/${var.cluster_name}-${var.environment}/performance"

  depends_on = [aws_ecs_cluster.this]
}
