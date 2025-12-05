# CloudWatch Log Group for ECS containers
# This is shared infrastructure - actual log streams will be created by ECS tasks
module "ecs_log_group" {
  source = "../../modules/cloudwatch-log-group"

  log_group_name    = "/ecs/devops2-g4-app-${terraform.workspace}"
  retention_in_days = 7
  environment       = terraform.workspace
  service_name      = "devops2-g4-app"
}
