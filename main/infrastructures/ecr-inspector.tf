# ECR Repository for api1
module "ecr_api1" {
  source = "../../modules/ecr"

  repository_name      = "devops2-g4-api1"
  environment          = terraform.workspace
  service_name         = "devops2-g4-api1"
  image_tag_mutability = "MUTABLE"
  scan_on_push         = true
  encryption_type      = "AES256"
  kms_key_arn          = null

  lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "any"
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
  
  force_delete = true
}

# ECR Repository for auth
module "ecr_auth" {
  source = "../../modules/ecr"

  repository_name      = "devops2-g4-auth"
  environment          = terraform.workspace
  service_name         = "devops2-g4-auth"
  image_tag_mutability = "MUTABLE"
  scan_on_push         = true
  encryption_type      = "AES256"
  kms_key_arn          = null

  lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "any"
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
  
  force_delete = true
}

# Amazon Inspector for ECR scanning
module "inspector" {
  source = "../../modules/inspector"

  account_id       = data.aws_caller_identity.current.account_id
  environment      = terraform.workspace
  service_name     = "devops2-g4-app"
  resource_types   = ["ECR"]
  create_sns_topic = true
  notification_email = null  # Set your email if you want notifications
}

# Data source to get current AWS account ID
data "aws_caller_identity" "current" {}
