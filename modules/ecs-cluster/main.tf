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

# Note: When Container Insights is enabled, ECS automatically creates
# the CloudWatch Log Group: /aws/ecs/containerinsights/{cluster-name}/performance
# No need to manage it with Terraform
