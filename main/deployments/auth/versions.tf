terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Optional: Configure remote state backend
  # backend "s3" {
  #   bucket         = "devops2-g4-remote-state-prod"
  #   key            = "deployments/auth/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "remote-state-locking-prod"
  # }
}
