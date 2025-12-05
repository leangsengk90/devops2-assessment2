# Security Group
resource "aws_security_group" "this" {
  name        = "${var.name}-${var.environment}"
  description = var.description
  vpc_id      = var.vpc_id

  tags = {
    Name        = "${var.name}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Ingress Rules
resource "aws_vpc_security_group_ingress_rule" "this" {
  count = length(var.ingress_rules)

  security_group_id = aws_security_group.this.id
  description       = var.ingress_rules[count.index].description

  # CIDR block rules
  cidr_ipv4   = lookup(var.ingress_rules[count.index], "cidr_ipv4", null)
  
  # Security group reference rules
  referenced_security_group_id = lookup(var.ingress_rules[count.index], "source_security_group_id", null)

  # Handle protocol -1 (all protocols) - must not specify ports
  from_port   = var.ingress_rules[count.index].protocol == "-1" ? -1 : var.ingress_rules[count.index].from_port
  to_port     = var.ingress_rules[count.index].protocol == "-1" ? -1 : var.ingress_rules[count.index].to_port
  ip_protocol = var.ingress_rules[count.index].protocol

  tags = {
    Name        = "${var.name}-ingress-${count.index}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}

# Egress Rules
resource "aws_vpc_security_group_egress_rule" "this" {
  count = length(var.egress_rules)

  security_group_id = aws_security_group.this.id
  description       = var.egress_rules[count.index].description

  # CIDR block rules
  cidr_ipv4   = lookup(var.egress_rules[count.index], "cidr_ipv4", null)
  
  # Security group reference rules
  referenced_security_group_id = lookup(var.egress_rules[count.index], "destination_security_group_id", null)

  # Handle protocol -1 (all protocols) - must not specify ports
  from_port   = var.egress_rules[count.index].protocol == "-1" ? -1 : var.egress_rules[count.index].from_port
  to_port     = var.egress_rules[count.index].protocol == "-1" ? -1 : var.egress_rules[count.index].to_port
  ip_protocol = var.egress_rules[count.index].protocol

  tags = {
    Name        = "${var.name}-egress-${count.index}-${var.environment}"
    Environment = var.environment
    Service     = var.service_name
  }
}
