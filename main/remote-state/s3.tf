
# S3 bucket for remote state
module "s3_bucket_remote_state" {
  source = "../../modules/s3"

  bucket_name = "devops2-g4-remote-state-${terraform.workspace}"
  force_destroy = true

  enable_public_access_block = true
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  enable_versioning = true
  status = "Enabled"

  enable_server_side_encryption_configuration = true
  sse_algorithm = "AES256"

  enable_cors_configuration = true
  allowed_methods = ["GET", "POST", "PUT", "DELETE"]
  allowed_origins = ["*"]
  allowed_headers = ["*"]
  max_age_seconds = 3000  

  enable_lifecycle_configuration = true
  lifecycle_rules = [
    {
      id     = "cleanup-old-versions"
      status = "Enabled"
      noncurrent_days = 30
    },
    {
      id     = "expire-temp-files"
      status = "Enabled"
      prefix = "temp/"
      expiration_days = 7
    }
  ]
}