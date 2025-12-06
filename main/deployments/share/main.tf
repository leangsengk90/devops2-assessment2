# Application Load Balancer
module "alb" {
  source = "../../../modules/alb"

  name                = "devops2-g4-share-alb"
  environment         = terraform.workspace
  service_name        = "devops2-g4-share"
  internal            = true
  security_group_ids  = [data.terraform_remote_state.infrastructure.outputs.alb_security_group_id]
  subnet_ids          = data.terraform_remote_state.infrastructure.outputs.private_subnet_ids
  vpc_id              = data.terraform_remote_state.infrastructure.outputs.vpc_id
  
  target_group_port            = 3004
  target_group_protocol        = "HTTP"
  health_check_path            = "/"
  health_check_protocol        = "HTTP"
  health_check_matcher         = "200"
  health_check_interval        = 30
  health_check_timeout         = 5
  health_check_healthy_threshold   = 2
  health_check_unhealthy_threshold = 3
  deregistration_delay         = 30
  enable_deletion_protection   = false
  enable_http2                 = true
}

# ECS Cluster
module "ecs_cluster" {
  source = "../../../modules/ecs-cluster"

  cluster_name              = "devops2-g4-share-cluster"
  environment               = terraform.workspace
  service_name              = "devops2-g4-share"
  enable_container_insights = true
  log_retention_days        = 7
}

# ECS Service with Auto Scaling
module "ecs_service" {
  source = "../../../modules/ecs-service"

  service_name        = "devops2-g4-share"
  environment         = terraform.workspace
  cluster_id          = module.ecs_cluster.cluster_id
  cluster_name        = module.ecs_cluster.cluster_name
  task_cpu            = "1024"
  task_memory         = "2048"
  execution_role_arn  = data.terraform_remote_state.infrastructure.outputs.ecs_task_execution_role_arn
  task_role_arn       = data.terraform_remote_state.infrastructure.outputs.ecs_task_role_arn
  
  # Container configuration
  container_name      = "share-app"
  container_image     = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-share-prod:1"  
  container_port      = 3004
  
  # Environment variables for the container
  environment_variables = [
    {
      name  = "APP_ENV"
      value = terraform.workspace
    },
    {
      name  = "PORT"
      value = "3004"
    }
  ]
  
  # Logging
  log_group_name      = data.terraform_remote_state.infrastructure.outputs.ecs_log_group_name
  aws_region          = var.aws_region
  
  # Network configuration
  subnet_ids          = data.terraform_remote_state.infrastructure.outputs.private_subnet_ids
  security_group_ids  = [data.terraform_remote_state.infrastructure.outputs.ecs_security_group_id]
  
  # Load balancer
  target_group_arn    = module.alb.target_group_arn
  
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

# API Gateway Route for share
module "api_gateway_route" {
  source = "../../../modules/api-gateway-route"

  api_gateway_id   = data.terraform_remote_state.infrastructure.outputs.api_gateway_id
  vpc_link_id      = data.terraform_remote_state.infrastructure.outputs.vpc_link_id
  alb_listener_arn = module.alb.http_listener_arn
  route_prefix     = "/share"
  service_name     = "devops2-g4-share"
  environment      = terraform.workspace
}
