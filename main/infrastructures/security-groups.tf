# Security Group for ALB (private)
module "alb_security_group" {
  source = "../../modules/security-group"

  name         = "devops2-g4-alb-sg"
  description  = "Security group for Application Load Balancer"
  vpc_id       = module.vpc.vpc_id
  environment  = terraform.workspace
  service_name = "devops2-g4-app"

  # Allow inbound from VPC Link
  ingress_rules = [
    {
      description  = "Allow HTTP from VPC Link"
      from_port    = 80
      to_port      = 80
      protocol     = "tcp"
      cidr_ipv4    = module.vpc.vpc_cidr
    },
    {
      description  = "Allow HTTPS from VPC Link"
      from_port    = 443
      to_port      = 443
      protocol     = "tcp"
      cidr_ipv4    = module.vpc.vpc_cidr
    }
  ]

  # Allow outbound to ECS tasks
  egress_rules = [
    {
      description                   = "Allow all outbound to ECS tasks"
      from_port                     = 0
      to_port                       = 65535
      protocol                      = "tcp"
      destination_security_group_id = module.ecs_security_group.security_group_id
    }
  ]
}

# Security Group for ECS Tasks
module "ecs_security_group" {
  source = "../../modules/security-group"

  name         = "devops2-g4-ecs-sg"
  description  = "Security group for ECS Fargate tasks"
  vpc_id       = module.vpc.vpc_id
  environment  = terraform.workspace
  service_name = "devops2-g4-app"

  # Allow inbound from ALB only
  ingress_rules = [
    {
      description              = "Allow traffic from ALB"
      from_port                = 0
      to_port                  = 65535
      protocol                 = "tcp"
      source_security_group_id = module.alb_security_group.security_group_id
    }
  ]

  # Allow all outbound (for ECR, CloudWatch, internet access via NAT)
  egress_rules = [
    {
      description = "Allow all outbound traffic"
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_ipv4   = "0.0.0.0/0"
    }
  ]
}

# Security Group for VPC Link
module "vpc_link_security_group" {
  source = "../../modules/security-group"

  name         = "devops2-g4-vpclink-sg"
  description  = "Security group for API Gateway VPC Link"
  vpc_id       = module.vpc.vpc_id
  environment  = terraform.workspace
  service_name = "devops2-g4-app"

  # Allow inbound HTTPS from internet (API Gateway managed service)
  ingress_rules = [
    {
      description = "Allow HTTPS from anywhere"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_ipv4   = "0.0.0.0/0"
    }
  ]

  # Allow outbound to ALB
  egress_rules = [
    {
      description                   = "Allow traffic to ALB"
      from_port                     = 0
      to_port                       = 65535
      protocol                      = "tcp"
      destination_security_group_id = module.alb_security_group.security_group_id
    }
  ]
}
