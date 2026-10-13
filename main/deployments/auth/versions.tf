terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Optional: Configure remote state backend
  backend "s3" {
    bucket         = "devops2-g4-remote-state-029637202701"
    key            = "deployments/auth/terraform.tfstate"
    region         = "ap-southeast-2"
    dynamodb_table = "remote-state-locking"
  }
}
