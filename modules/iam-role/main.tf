# IAM Role
resource "aws_iam_role" "this" {
  name               = "${var.role_name}-${var.environment}"
  assume_role_policy = var.assume_role_policy

  tags = {
    Name        = "${var.role_name}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Attach AWS Managed Policies
resource "aws_iam_role_policy_attachment" "managed_policies" {
  count = length(var.managed_policy_arns)

  role       = aws_iam_role.this.name
  policy_arn = var.managed_policy_arns[count.index]
}

# Create and Attach Custom Inline Policy
resource "aws_iam_role_policy" "inline_policy" {
  count = var.inline_policy != null ? 1 : 0

  name   = "${var.role_name}-inline-policy-${var.environment}"
  role   = aws_iam_role.this.id
  policy = var.inline_policy
}
