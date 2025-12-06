# AWS Infrastructure Cost Analysis & Optimization

## Current Infrastructure Overview

**Region:** us-east-1  
**Environment:** Production  
**Services:** 6 microservices (api1, auth, profile, messenger, finance, share)

---

## Monthly Cost Breakdown (Estimated)

### 1. **Amazon ECS (Fargate)**

6 services × 2-10 tasks each

**Baseline (2 tasks per service = 12 tasks total):**

- vCPU: 1 vCPU per task = 12 vCPU
- Memory: 2 GB per task = 24 GB
- Running 24/7

**Cost Calculation:**

```
vCPU Cost: 12 vCPU × $0.04048/vCPU/hour × 730 hours = $354.82/month
Memory Cost: 24 GB × $0.004445/GB/hour × 730 hours = $77.88/month

Total ECS Fargate (baseline): $432.70/month
```

**With Auto-scaling (average 5 tasks per service = 30 tasks):**

```
vCPU: 30 × $0.04048 × 730 = $887.05/month
Memory: 60 GB × $0.004445 × 730 = $194.71/month

Total ECS Fargate (scaled): $1,081.76/month
```

---

### 2. **Application Load Balancers (ALB)**

6 ALBs (one per service)

**Cost:**

```
Fixed Cost: 6 ALBs × $0.0225/hour × 730 hours = $98.55/month
LCU (Load Balancer Capacity Units):
  - Estimated: 10 LCUs per ALB × 6 = 60 LCUs
  - Cost: 60 × $0.008/hour × 730 = $350.40/month

Total ALB Cost: $448.95/month
```

---

### 3. **API Gateway (HTTP API)**

1 shared API Gateway for all services

**Assumptions:**

- 10 million requests/month
- Average payload: 50 KB

**Cost:**

```
First 1M requests: Free
Next 9M requests: 9,000,000 × $0.001/million = $9.00/month

Total API Gateway Cost: $9.00/month
```

---

### 4. **NAT Gateway**

2 NAT Gateways (for HA across AZs)

**Cost:**

```
Fixed Cost: 2 × $0.045/hour × 730 hours = $65.70/month
Data Processing:
  - Estimated 500 GB/month (container pulls, external APIs)
  - Cost: 500 GB × $0.045/GB = $22.50/month

Total NAT Gateway Cost: $88.20/month
```

---

### 5. **VPC Link**

1 shared VPC Link

**Cost:**

```
Fixed: $0.01/hour × 730 hours = $7.30/month
Data Transfer: Included in API Gateway pricing

Total VPC Link Cost: $7.30/month
```

---

### 6. **Elastic Container Registry (ECR)**

6 repositories

**Storage:**

```
Estimated: 10 GB total (all images)
Cost: 10 GB × $0.10/GB/month = $1.00/month

Data Transfer:
  - Container image pulls (within region): Free
  - To internet: Negligible for private deployments

Total ECR Cost: $1.00/month
```

---

### 7. **CloudWatch**

**Logs:**

```
Ingestion: 50 GB/month × $0.50/GB = $25.00/month
Storage (7 days retention): ~5 GB × $0.03/GB = $0.15/month

Total Logs: $25.15/month
```

**Metrics & Container Insights:**

```
Custom Metrics: 100 metrics × $0.30 = $30.00/month
Container Insights: 6 clusters × ~$10/cluster = $60.00/month

Total Metrics: $90.00/month
```

**Alarms:**

```
24 alarms (4 per service) × $0.10/alarm = $2.40/month
```

**Total CloudWatch Cost: $117.55/month**

---

### 8. **Amazon Inspector**

ECR image scanning

**Cost:**

```
Scans: ~30 scans/month (5 per repo avg)
Cost: 30 × $0.09 = $2.70/month

Total Inspector Cost: $2.70/month
```

---

### 9. **Data Transfer**

**Assumptions:**

- Inter-AZ traffic: 200 GB/month
- To Internet (through NAT): Already counted in NAT Gateway

**Cost:**

```
Inter-AZ: 200 GB × $0.01/GB = $2.00/month

Total Data Transfer Cost: $2.00/month
```

---

## **TOTAL MONTHLY COST SUMMARY**

### Baseline Configuration (2 tasks per service):

```
ECS Fargate:              $432.70
ALB:                      $448.95
API Gateway:              $9.00
NAT Gateway:              $88.20
VPC Link:                 $7.30
ECR:                      $1.00
CloudWatch:               $117.55
Inspector:                $2.70
Data Transfer:            $2.00
─────────────────────────────────
TOTAL:                    $1,109.40/month
```

### Average Load (5 tasks per service):

```
ECS Fargate:              $1,081.76
ALB:                      $448.95
API Gateway:              $9.00
NAT Gateway:              $88.20
VPC Link:                 $7.30
ECR:                      $1.00
CloudWatch:               $117.55
Inspector:                $2.70
Data Transfer:            $2.00
─────────────────────────────────
TOTAL:                    $1,758.46/month
```

### Peak Load (10 tasks per service):

```
ECS Fargate:              $2,163.52
ALB:                      $448.95
API Gateway:              $9.00
NAT Gateway:              $88.20
VPC Link:                 $7.30
ECR:                      $1.00
CloudWatch:               $117.55
Inspector:                $2.70
Data Transfer:            $2.00
─────────────────────────────────
TOTAL:                    $2,840.22/month
```

---

## Cost Optimization Strategies

### 🎯 **HIGH IMPACT - Immediate Savings**

#### 1. **Consolidate Load Balancers** (Save ~$400/month)

**Current:** 6 separate ALBs (one per service)  
**Optimized:** 1 shared ALB with path-based routing

**Implementation:**

```hcl
# Single ALB with listener rules for each service
resource "aws_lb_listener_rule" "api1" {
  listener_arn = aws_lb_listener.shared.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api1.arn
  }

  condition {
    path_pattern {
      values = ["/api1/*"]
    }
  }
}
```

**Savings:**

```
Before: 6 × ($0.0225/hour × 730 + ~$58 LCU) = $448.95/month
After:  1 × ($0.0225/hour × 730 + ~$100 LCU) = $96.43/month
SAVINGS: $352.52/month (~79% reduction)
```

---

#### 2. **Use Fargate Spot for Non-Critical Services** (Save ~40-70%)

**Current:** All tasks use on-demand Fargate  
**Optimized:** Use Spot for dev/test workloads or fault-tolerant services

**Implementation:**

```hcl
resource "aws_ecs_service" "this" {
  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 70  # 70% Spot
    base              = 0
  }

  capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 30  # 30% On-demand
    base              = 1   # At least 1 on-demand
  }
}
```

**Savings:**

```
Spot Discount: ~70% off Fargate pricing
If 70% of tasks use Spot: $1,081.76 × 0.70 × 0.70 = $529.43 saved
SAVINGS: $529.43/month
```

---

#### 3. **Reduce NAT Gateway Costs** (Save ~$65/month)

**Option A:** Use VPC Endpoints for AWS services

```hcl
# S3 VPC Endpoint (Gateway - Free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.us-east-1.s3"
  route_table_ids = [aws_route_table.private.id]
}

# ECR VPC Endpoints (Interface - $0.01/hour each)
resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.us-east-1.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private[*].id
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
}
```

**Savings:**

```
NAT Gateway data processing: $22.50/month
ECR VPC Endpoint: $0.01/hour × 730 = $7.30/month
S3 VPC Endpoint: Free
NET SAVINGS: $15.20/month + reduced NAT processing
```

**Option B:** Single NAT Gateway (non-HA)

```
Current: 2 NAT Gateways = $65.70/month
Optimized: 1 NAT Gateway = $32.85/month
SAVINGS: $32.85/month (⚠️ Reduces HA)
```

---

#### 4. **Right-size ECS Tasks** (Save ~20-30%)

**Analysis:** Monitor actual CPU/Memory usage

```bash
# Check CloudWatch metrics for actual utilization
# If average CPU < 50% and Memory < 50%, downsize

# Current: 1 vCPU, 2 GB
# Optimized: 0.5 vCPU, 1 GB (if workload permits)
```

**Savings:**

```
50% resource reduction = 50% cost reduction
$1,081.76 × 0.50 = $540.88 saved
SAVINGS: $540.88/month
```

---

### 💡 **MEDIUM IMPACT - Configuration Changes**

#### 5. **Optimize CloudWatch Logs Retention**

```hcl
resource "aws_cloudwatch_log_group" "ecs" {
  retention_in_days = 3  # Instead of 7
}
```

**Savings:** ~$10-15/month

#### 6. **Use Reserved Capacity for Fargate** (if available in future)

- 1-year commitment: ~30% savings
- 3-year commitment: ~50% savings
- Currently not available for Fargate, but monitor AWS announcements

#### 7. **Reduce Container Insights Granularity**

```hcl
# Disable for non-production or less critical services
enable_container_insights = false
```

**Savings:** $10/cluster × disabled clusters

#### 8. **Optimize Auto-scaling Thresholds**

```hcl
# More aggressive scale-down
autoscaling_cpu_threshold_down = 20  # Instead of 30
autoscaling_memory_threshold_down = 20
scale_down_cooldown = 180  # Instead of 300
```

**Savings:** Faster scale-down = lower average task count

---

### 🔧 **LOW IMPACT - Operational Improvements**

#### 9. **Image Optimization**

- Use multi-stage Docker builds
- Minimize layer sizes
- Use alpine-based images
- Remove unnecessary dependencies

**Impact:** Reduce ECR storage and faster deployments

#### 10. **API Gateway Caching**

```hcl
resource "aws_apigatewayv2_stage" "default" {
  # Enable caching for repeated requests
  default_route_settings {
    data_trace_enabled = false  # Reduce logs
  }
}
```

#### 11. **Scheduled Scaling for Non-Production**

```hcl
# Scale down during off-hours
resource "aws_appautoscaling_scheduled_action" "scale_down_night" {
  name               = "scale-down-night"
  service_namespace  = "ecs"
  resource_id        = "service/${var.cluster_name}/${var.service_name}"
  scalable_dimension = "ecs:service:DesiredCount"
  schedule           = "cron(0 20 * * ? *)"  # 8 PM UTC

  scalable_target_action {
    min_capacity = 1
    max_capacity = 2
  }
}
```

---

## Optimized Architecture Cost Comparison

### **Original Architecture:**

```
6 ALBs + On-demand Fargate + 2 NAT Gateways = $1,758.46/month
```

### **Optimized Architecture:**

```
1 Shared ALB:                           $96.43
70% Fargate Spot + 30% On-demand:       $552.33
1 NAT Gateway + VPC Endpoints:          $40.00
API Gateway:                            $9.00
VPC Link:                               $7.30
ECR:                                    $1.00
CloudWatch (optimized):                 $80.00
Inspector:                              $2.70
Data Transfer:                          $2.00
─────────────────────────────────────────────
TOTAL:                                  $790.76/month
```

### **TOTAL POTENTIAL SAVINGS: $967.70/month (55% reduction)**

---

## Implementation Priority

### Phase 1 (Week 1): **Consolidate ALBs**

- **Effort:** Medium
- **Savings:** $352/month
- **Risk:** Low

### Phase 2 (Week 2): **Enable Fargate Spot**

- **Effort:** Low
- **Savings:** $529/month
- **Risk:** Medium (handle interruptions)

### Phase 3 (Week 3): **VPC Endpoints**

- **Effort:** Low
- **Savings:** $15-30/month
- **Risk:** Low

### Phase 4 (Week 4): **Right-size Tasks**

- **Effort:** High (requires monitoring/analysis)
- **Savings:** $540/month
- **Risk:** Medium (performance impact)

### Phase 5 (Ongoing): **CloudWatch & Auto-scaling Tuning**

- **Effort:** Low
- **Savings:** $20-40/month
- **Risk:** Low

---

## Cost Monitoring & Alerts

### Set up AWS Budgets:

```hcl
resource "aws_budgets_budget" "monthly_cost" {
  name              = "monthly-infrastructure-budget"
  budget_type       = "COST"
  limit_amount      = "2000"
  limit_unit        = "USD"
  time_period_start = "2025-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["devops@example.com"]
  }
}
```

### CloudWatch Cost Anomaly Detection:

- Enable AWS Cost Anomaly Detection
- Set up SNS alerts for unusual spending

### Tag Resources for Cost Allocation:

```hcl
tags = {
  Service     = "api1"
  Environment = "production"
  CostCenter  = "engineering"
  ManagedBy   = "terraform"
}
```

---

## Annual Cost Projection

### Current Architecture:

```
Monthly: $1,758.46
Annual:  $21,101.52
```

### Optimized Architecture:

```
Monthly: $790.76
Annual:  $9,489.12

ANNUAL SAVINGS: $11,612.40 (55% reduction)
```

---

## Recommendations Summary

✅ **Immediate Actions:**

1. Consolidate to 1 shared ALB
2. Implement Fargate Spot for 70% of workload
3. Add VPC Endpoints for ECR/S3

✅ **Short-term (1-3 months):**

1. Analyze and right-size task definitions
2. Optimize CloudWatch retention
3. Implement scheduled scaling

✅ **Long-term:**

1. Monitor for Fargate Reserved Capacity availability
2. Consider AWS Savings Plans
3. Regular cost reviews (monthly)

---

## Additional Resources

- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)
- [AWS Well-Architected Tool](https://aws.amazon.com/well-architected-tool/)
- [Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [ALB Pricing](https://aws.amazon.com/elasticloadbalancing/pricing/)
