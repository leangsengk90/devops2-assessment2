# Target Group and Listener Rule for shared ALB
module "alb_target_group" {
  source = "../../../modules/alb-target-group"

  service_name            = "devops2-g4-messenger"
  environment             = terraform.workspace
  vpc_id                  = data.terraform_remote_state.infrastructure.outputs.vpc_id
  alb_listener_arn        = data.terraform_remote_state.infrastructure.outputs.shared_alb_listener_arn
  container_port          = 3002
  listener_rule_priority  = 400
  path_patterns           = ["/messenger", "/messenger/*"]
  
  health_check_path                = "/"
  health_check_matcher             = "200"
  health_check_interval            = 30
  health_check_timeout             = 5
  health_check_healthy_threshold   = 2
  health_check_unhealthy_threshold = 3
  deregistration_delay             = 30
}

# ECS Cluster
module "ecs_cluster" {
  source = "../../../modules/ecs-cluster"

  cluster_name              = "devops2-g4-messenger-cluster"
  environment               = terraform.workspace
  service_name              = "devops2-g4-messenger"
  enable_container_insights = true
  log_retention_days        = 7
}

# ECS Service with Auto Scaling
module "ecs_service" {
  source = "../../../modules/ecs-service"

  service_name        = "devops2-g4-messenger"
  environment         = terraform.workspace
  cluster_id          = module.ecs_cluster.cluster_id
  cluster_name        = module.ecs_cluster.cluster_name
  task_cpu            = "1024"
  task_memory         = "2048"
  execution_role_arn  = data.terraform_remote_state.infrastructure.outputs.ecs_task_execution_role_arn
  task_role_arn       = data.terraform_remote_state.infrastructure.outputs.ecs_task_role_arn
  
  # Container configuration
  container_name      = "messenger-app"
  container_image     = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-messenger-prod:6"  
  container_port      = 3002
  
  # Environment variables for the container
  environment_variables = [
    {
      name  = "APP_ENV"
      value = terraform.workspace
    },
    {
      name  = "PORT"
      value = "3002"
    }
  ]
  
  # Logging
  log_group_name      = data.terraform_remote_state.infrastructure.outputs.ecs_log_group_name
  aws_region          = var.aws_region
  
  # Network configuration
  subnet_ids          = data.terraform_remote_state.infrastructure.outputs.private_subnet_ids
  security_group_ids  = [data.terraform_remote_state.infrastructure.outputs.ecs_security_group_id]
  
  # Load balancer
  target_group_arn    = module.alb_target_group.target_group_arn
  
  # Service configuration
  desired_count                    = 2
  deployment_maximum_percent       = 200
  deployment_minimum_healthy_percent = 100
  health_check_grace_period        = 60
  
  # Auto scaling
  autoscaling_min_capacity = 2
  autoscaling_max_capacity = 10
  scale_up_cooldown        = 60
  scale_down_cooldown      = 300
}

# API Gateway Route for messenger
module "api_gateway_route" {
  source = "../../../modules/api-gateway-route"

  api_gateway_id   = data.terraform_remote_state.infrastructure.outputs.api_gateway_id
  vpc_link_id      = data.terraform_remote_state.infrastructure.outputs.vpc_link_id
  alb_listener_arn = data.terraform_remote_state.infrastructure.outputs.shared_alb_listener_arn
  route_prefix     = "/messenger"
  service_name     = "devops2-g4-messenger"
  environment      = terraform.workspace
}
