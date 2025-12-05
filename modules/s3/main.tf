
# Create an S3 bucket with specific configurations
resource "aws_s3_bucket" "this" {
  bucket        = "${var.bucket_name}"
  force_destroy = var.force_destroy
  tags = {
    Service        = "${var.bucket_name}"
    Environment    = "${terraform.workspace}"
  }
}

# Set public access block configuration
resource "aws_s3_bucket_public_access_block" "this" {
  count = var.enable_public_access_block ? 1 : 0
  bucket = aws_s3_bucket.this.id
  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}

# Enable versioning on the S3 bucket
resource "aws_s3_bucket_versioning" "this" {
  count = var.enable_versioning ? 1 : 0
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "${var.status}"
  }
}

# Set server-side encryption configuration
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  count = var.enable_server_side_encryption_configuration ? 1 : 0
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "${var.sse_algorithm}"
    }
  }
}

# Configure CORS for the S3 bucket
resource "aws_s3_bucket_cors_configuration" "this" {
  count = var.enable_cors_configuration ? 1 : 0
  bucket = aws_s3_bucket.this.id
  cors_rule {
    allowed_methods = var.allowed_methods
    allowed_origins = var.allowed_origins
    allowed_headers = var.allowed_headers
    max_age_seconds = var.max_age_seconds
  }
}

# Set lifecycle rules for the S3 bucket
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  count = var.enable_lifecycle_configuration ? 1 : 0
  bucket = aws_s3_bucket.this.id
  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      id     = rule.value.id
      status = rule.value.status

      # Optional block: filter.prefix
      dynamic "filter" {
        for_each = rule.value.prefix != null ? [rule.value.prefix] : []
        content {
          prefix = filter.value
        }
      }

      # Optional block: expiration
      dynamic "expiration" {
        for_each = rule.value.expiration_days != null ? [rule.value.expiration_days] : []
        content {
          days = expiration.value
        }
      }

      # Optional block: noncurrent_version_expiration
      dynamic "noncurrent_version_expiration" {
        for_each = rule.value.noncurrent_days != null ? [rule.value.noncurrent_days] : []
        content {
          noncurrent_days = noncurrent_version_expiration.value
        }
      }
    }
  }
}
