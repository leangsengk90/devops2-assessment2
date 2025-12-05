
# DynamoDB table for Terraform state locking
module "dynamodb_table_locking" {
  source = "../../modules/dynamodb"

  dynamodb_table_name               = "remote-state-locking-${terraform.workspace}"
  billing_mode                      = "PAY_PER_REQUEST"
  hash_key                          = "LockID"
  hash_key_type                     = "S"
  ttl_attribute_name                = "TimeToExist"
  ttl_enabled                       = true
  server_side_encryption_enabled    = true
}