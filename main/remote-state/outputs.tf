# S3 bucket for remote state
output "s3_bucket_remote_state_id" {
  value = module.s3_bucket_remote_state.aws_s3_bucket_this.id
}

output "s3_bucket_remote_state_arn" {
  value = module.s3_bucket_remote_state.aws_s3_bucket_this.arn
}

output "s3_bucket_remote_state_bucket_domain_name" {
  value = module.s3_bucket_remote_state.aws_s3_bucket_this.bucket_domain_name
}

# DynamoDB table for remote state locking
output "dynamodb_table_locking_id" {
  value = module.dynamodb_table_locking.aws_dynamodb_table_this.id
}

output "dynamodb_table_locking_arn" {
  value = module.dynamodb_table_locking.aws_dynamodb_table_this.arn
} 

output "dynamodb_table_locking_name" {
  value = module.dynamodb_table_locking.aws_dynamodb_table_this.name
} 

