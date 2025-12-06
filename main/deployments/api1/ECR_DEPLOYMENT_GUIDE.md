# API1 Service Deployment Guide

## Overview

This guide walks you through deploying the API1 microservice to AWS ECS Fargate with:

- ✅ Shared ALB with header-based routing
- ✅ API Gateway with path rewriting
- ✅ Auto-scaling from 2-10 tasks
- ✅ ECR image scanning with Amazon Inspector
- ✅ CloudWatch Container Insights

**Architecture:** API Gateway → VPC Link → Shared ALB → Target Group → ECS Tasks

---

## Prerequisites

- ✅ AWS CLI configured with appropriate credentials
- ✅ Docker installed locally
- ✅ Terraform installed
- ✅ Shared infrastructure deployed (`main/infrastructures`)

---

## Step 1: Verify Shared Infrastructure

Before deploying the API1 service, ensure shared infrastructure is deployed:

```bash
cd main/infrastructures
terraform workspace select prod

# Verify infrastructure outputs
terraform output

# Required outputs:
# - shared_alb_arn
# - shared_alb_listener_arn
# - api_gateway_id
# - vpc_link_id
# - ecr_api1_repository_url
```

If infrastructure is not deployed, deploy it first:

```bash
terraform init
terraform workspace select prod || terraform workspace new prod
terraform plan -var-file=../../variables/global.tfvars -out=../../plans/infrastructure-prod.plan
terraform apply ../../plans/infrastructure-prod.plan
```

---

## Step 2: Get ECR Repository URL

Retrieve your ECR repository URL for API1:

```bash
cd main/infrastructures
terraform output ecr_api1_repository_url
```

**Example output:**

```
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod
```

---

## Step 3: Build and Push Docker Image

### 3.1 Authenticate Docker to ECR

```bash
# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Authenticate Docker
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
```

**Expected output:** `Login Succeeded`

---

### 3.2 Prepare Your Application

For this example, we'll use nginx:alpine. Replace with your own application if needed.

**Create a simple Dockerfile (if you don't have one):**

```dockerfile
FROM nginx:alpine

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/nginx.conf

# Copy static content if needed
# COPY dist/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

### 3.3 Build Docker Image

```bash
# Navigate to your application directory
cd /path/to/your/api1-app

# Build the image
docker build -t devops2-g4-api1:latest .

# Verify the image was built
docker images | grep devops2-g4-api1
```

---

### 3.4 Tag for ECR

```bash
# Get ECR repository URL from infrastructure output
ECR_URL=$(cd ../../infrastructures && terraform output -raw ecr_api1_repository_url)

# Tag the image
docker tag devops2-g4-api1:latest ${ECR_URL}:latest

# Optional: Use version tags for better tracking
docker tag devops2-g4-api1:latest ${ECR_URL}:v1.0.0
```

---

### 3.5 Push to ECR

```bash
# Push latest tag
docker push ${ECR_URL}:latest

# Push version tag (if you created one)
docker push ${ECR_URL}:v1.0.0
```

**Amazon Inspector will automatically scan the image for vulnerabilities.**

---

### 3.6 Verify Image in ECR

```bash
# List images in the repository
aws ecr describe-images \
  --repository-name devops2-g4-api1-prod \
  --region us-east-1 \
  --query 'imageDetails[*].[imageTags[0],imagePushedAt]' \
  --output table
```

---

## Step 4: Configure Service Deployment

The API1 service is already configured in `main/deployments/api1/main.tf` with:

- **Container Port:** 80 (nginx default)
- **Listener Priority:** 100
- **Path Patterns:** `/api1`, `/api1/*`
- **Header:** `X-Service-Name: devops2-g4-api1`
- **Auto-scaling:** 2-10 tasks based on CPU/Memory

**Key Configuration (already set in main.tf):**

```hcl
# Target Group and Listener Rule
module "alb_target_group" {
  source = "../../../modules/alb-target-group"

  service_name            = "devops2-g4-api1"
  environment             = terraform.workspace
  vpc_id                  = data.terraform_remote_state.infrastructure.outputs.vpc_id
  alb_listener_arn        = data.terraform_remote_state.infrastructure.outputs.shared_alb_listener_arn
  container_port          = 80
  listener_rule_priority  = 100
  path_patterns           = ["/api1", "/api1/*"]
  health_check_path       = "/"
}

# ECS Service
module "ecs_service" {
  source = "../../../modules/ecs-service"

  container_image = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest"
  container_port  = 80
  task_cpu        = "1024"    # 1 vCPU
  task_memory     = "2048"    # 2 GB
  desired_count   = 2
  autoscaling_min_capacity = 2
  autoscaling_max_capacity = 10
}
```

---

## Step 5: Update Container Image URI (If Needed)

If your ECR repository URL is different, update `main.tf`:

```bash
cd main/deployments/api1
```

**Find and update the container_image line (around line 54):**

```hcl
# Before:
container_image = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest"

# After (use your actual ECR URL):
container_image = "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest"

# Or with version tag:
container_image = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:v1.0.0"
```

---

## Step 6: Deploy API1 Service

### 6.1 Initialize Terraform

```bash
cd main/deployments/api1
terraform init
```

---

### 6.2 Select Workspace

```bash
terraform workspace select prod || terraform workspace new prod
```

---

### 6.3 Plan Deployment

```bash
terraform plan \
  -var-file=../../../variables/global.tfvars \
  -out=../../../plans/api1-prod.plan
```

**Review the plan output:**

- ✅ Target group creation
- ✅ ALB listener rule creation (priority 100)
- ✅ ECS cluster creation
- ✅ ECS service creation
- ✅ Auto-scaling configuration
- ✅ CloudWatch alarms
- ✅ API Gateway route creation

---

### 6.4 Apply Deployment

```bash
terraform apply ../../../plans/api1-prod.plan
```

**Wait for deployment to complete (2-5 minutes).**

---

### 6.5 Get Service Outputs

```bash
terraform output
```

**Important outputs:**

- `api_invoke_url` - Your public API endpoint
- `ecs_cluster_name` - ECS cluster name
- `ecs_service_name` - ECS service name
- `target_group_arn` - Target group ARN

---

## Step 7: Verify Deployment

### 7.1 Check ECS Service Status

```bash
# Get cluster and service names
CLUSTER=$(terraform output -raw ecs_cluster_name)
SERVICE=$(terraform output -raw ecs_service_name)

# Check service status
aws ecs describe-services \
  --cluster ${CLUSTER} \
  --services ${SERVICE} \
  --query 'services[0].[serviceName,status,runningCount,desiredCount]' \
  --output table
```

**Expected output:** `runningCount` should equal `desiredCount` (2)

---

### 7.2 Check Target Group Health

```bash
# Get target group ARN
TG_ARN=$(terraform output -raw target_group_arn)

# Check target health
aws elbv2 describe-target-health \
  --target-group-arn ${TG_ARN} \
  --query 'TargetHealthDescriptions[*].[Target.Id,TargetHealth.State,TargetHealth.Reason]' \
  --output table
```

**Expected output:** All targets should be `healthy`

---

### 7.3 Test API Endpoint

```bash
# Get API Gateway endpoint
API_URL=$(terraform output -raw api_invoke_url)

# Test the endpoint
curl ${API_URL}

# Or with full URL
curl https://xxxxx.execute-api.us-east-1.amazonaws.com/api1
```

**Expected output:** Your application's response (nginx welcome page for default config)

---

### 7.4 Check CloudWatch Logs

```bash
# View recent logs
aws logs tail /aws/ecs/devops2-g4-app --follow --filter-pattern "api1"
```

---

## Step 8: Monitor and Scale

### 8.1 View Container Insights

```bash
# Open Container Insights in AWS Console
# CloudWatch → Container Insights → ECS Clusters → devops2-g4-api1-cluster-prod
```

**Metrics to monitor:**

- CPU utilization
- Memory utilization
- Network traffic
- Task count

---

### 8.2 Check Auto-scaling Alarms

```bash
# List CloudWatch alarms for API1
aws cloudwatch describe-alarms \
  --alarm-name-prefix "devops2-g4-api1" \
  --query 'MetricAlarms[*].[AlarmName,StateValue]' \
  --output table
```

**Alarms created:**

- `devops2-g4-api1-cpu-high-prod` - Triggers scale up at 70% CPU
- `devops2-g4-api1-cpu-low-prod` - Triggers scale down at 30% CPU
- `devops2-g4-api1-memory-high-prod` - Triggers scale up at 70% Memory
- `devops2-g4-api1-memory-low-prod` - Triggers scale down at 30% Memory

---

### 8.3 View Inspector Findings

```bash
# List ECR image scan findings
aws ecr describe-image-scan-findings \
  --repository-name devops2-g4-api1-prod \
  --image-id imageTag=latest \
  --query 'imageScanFindings.findings[*].[severity,name,description]' \
  --output table
```

**Or view in AWS Console:**  
Amazon Inspector → Findings → Filter by repository

---

## Step 9: Update Application

When you need to deploy a new version:

### 9.1 Build and Push New Image

```bash
# Build new version
cd /path/to/your/api1-app
docker build -t devops2-g4-api1:v2.0.0 .

# Tag for ECR
ECR_URL=$(cd ../../main/infrastructures && terraform output -raw ecr_api1_repository_url)
docker tag devops2-g4-api1:v2.0.0 ${ECR_URL}:v2.0.0
docker tag devops2-g4-api1:v2.0.0 ${ECR_URL}:latest

# Push to ECR
docker push ${ECR_URL}:v2.0.0
docker push ${ECR_URL}:latest
```

---

### 9.2 Update main.tf

```bash
cd main/deployments/api1
```

**Update container_image in main.tf:**

```hcl
container_image = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:v2.0.0"
```

---

### 9.3 Deploy Update

```bash
terraform plan -var-file=../../../variables/global.tfvars -out=../../../plans/api1-prod.plan
terraform apply ../../../plans/api1-prod.plan
```

**ECS will perform a rolling update with zero downtime.**

---

### 9.4 Monitor Deployment

```bash
# Watch deployment progress
watch -n 2 'aws ecs describe-services \
  --cluster devops2-g4-api1-cluster-prod \
  --services devops2-g4-api1-service-prod \
  --query "services[0].deployments" \
  --output table'
```

---

## Troubleshooting

### Issue: Targets Unhealthy in Target Group

**Symptoms:** Targets show as "unhealthy" in target group

**Solutions:**

1. **Check container is running:**

   ```bash
   aws ecs list-tasks --cluster devops2-g4-api1-cluster-prod
   ```

2. **Check container logs:**

   ```bash
   aws logs tail /aws/ecs/devops2-g4-app --follow
   ```

3. **Verify health check path:**

   - Default health check: `/`
   - Ensure your app responds with HTTP 200 at this path

4. **Check security groups:**
   - ECS security group must allow traffic from ALB security group on port 80

---

### Issue: Service Not Found (404)

**Symptoms:** API Gateway returns "Service not found"

**Solutions:**

1. **Verify API Gateway route exists:**

   ```bash
   cd main/infrastructures
   terraform output api_gateway_id

   aws apigatewayv2 get-routes --api-id <API_ID> \
     --query 'Items[?contains(RouteKey, `api1`)]'
   ```

2. **Check ALB listener rule:**

   ```bash
   aws elbv2 describe-rules \
     --listener-arn $(cd main/infrastructures && terraform output -raw shared_alb_listener_arn) \
     --query 'Rules[?Priority==`100`]'
   ```

3. **Verify deployment completed:**
   ```bash
   cd main/deployments/api1
   terraform output
   ```

---

### Issue: Cannot Pull Container Image

**Symptoms:** Task fails with "CannotPullContainerError"

**Solutions:**

1. **Verify image exists in ECR:**

   ```bash
   aws ecr describe-images --repository-name devops2-g4-api1-prod
   ```

2. **Check task execution role permissions:**

   - Role must have `ecr:GetAuthorizationToken`
   - Role must have `ecr:BatchGetImage`
   - Role must have `ecr:GetDownloadUrlForLayer`

3. **Ensure NAT Gateway is configured:**
   - ECS tasks in private subnets need NAT for ECR access

---

### Issue: Auto-scaling Not Working

**Symptoms:** Service doesn't scale despite high CPU/Memory

**Solutions:**

1. **Check CloudWatch alarms:**

   ```bash
   aws cloudwatch describe-alarms \
     --alarm-name-prefix "devops2-g4-api1" \
     --state-value ALARM
   ```

2. **Verify metrics are being collected:**

   - Check Container Insights is enabled
   - Wait at least 5 minutes for metrics to populate

3. **Review auto-scaling configuration:**
   ```bash
   aws application-autoscaling describe-scalable-targets \
     --service-namespace ecs \
     --resource-id service/devops2-g4-api1-cluster-prod/devops2-g4-api1-service-prod
   ```

---

## Configuration Reference

### Resource Configuration (in main.tf)

| Parameter                 | Value         | Description                     |
| ------------------------- | ------------- | ------------------------------- |
| **Container Port**        | 80            | nginx default port              |
| **Task CPU**              | 1024 (1 vCPU) | CPU units for each task         |
| **Task Memory**           | 2048 (2 GB)   | Memory for each task            |
| **Desired Count**         | 2             | Initial number of tasks         |
| **Min Capacity**          | 2             | Minimum tasks during scale down |
| **Max Capacity**          | 10            | Maximum tasks during scale up   |
| **Health Check Path**     | `/`           | ALB health check endpoint       |
| **Health Check Interval** | 30 seconds    | Time between health checks      |
| **Listener Priority**     | 100           | ALB listener rule priority      |

### Auto-scaling Thresholds

| Metric       | Scale Up    | Scale Down  |
| ------------ | ----------- | ----------- |
| **CPU**      | > 70%       | < 30%       |
| **Memory**   | > 70%       | < 30%       |
| **Cooldown** | 300 seconds | 300 seconds |

---

## Additional Resources

- **Architecture Diagram**: See `../../../diagram.txt`
- **Cost Analysis**: See `../../../COST_ANALYSIS.md`
- **Infrastructure Summary**: See `../../../INFRASTRUCTURE_SUMMARY.md`
- **AWS ECS Documentation**: https://docs.aws.amazon.com/ecs/
- **API Gateway HTTP APIs**: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html

---

## Next Steps

After API1 is deployed:

1. ✅ Deploy other services (auth, profile, messenger, finance, share)
2. ✅ Set up monitoring dashboards
3. ✅ Configure alerts and notifications
4. ✅ Implement CI/CD pipeline
5. ✅ Review and optimize costs

---

**Document Version:** 2.0  
**Last Updated:** December 6, 2025  
**Architecture:** Shared ALB with header-based routing
