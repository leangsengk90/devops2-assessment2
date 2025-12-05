
# DynamoDB Table for lock state management
resource "aws_dynamodb_table" "this" {
  name         = var.dynamodb_table_name
  billing_mode = var.billing_mode
  hash_key     = var.hash_key

  attribute {
    name = var.hash_key
    type = var.hash_key_type
  }

  ttl {
    attribute_name = var.ttl_attribute_name
    enabled        = var.ttl_enabled
  }

  server_side_encryption {
    enabled = var.server_side_encryption_enabled
  }

  tags = {
    Service     = var.dynamodb_table_name
    Environment = terraform.workspace
  }
}
