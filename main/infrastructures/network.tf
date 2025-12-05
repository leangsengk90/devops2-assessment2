# VPC Module
module "vpc" {
  source = "../../modules/vpc"

  name               = "devops2-g4-app"
  environment        = terraform.workspace
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b"]
  
  # Public subnets for NAT Gateway
  public_subnet_cidrs = [
    "10.0.1.0/24",  # us-east-1a
    "10.0.2.0/24"   # us-east-1b
  ]
  
  # Private subnets for ALB and ECS tasks
  private_subnet_cidrs = [
    "10.0.11.0/24", # us-east-1a
    "10.0.12.0/24"  # us-east-1b
  ]
  
  enable_nat_gateway = true
}
