# API1 Deployment

This deployment creates a complete ECS Fargate application with API Gateway, ALB, and auto scaling.

## Architecture

```
Internet → API Gateway (HTTP API) → VPC Link → Private ALB → ECS Fargate Tasks
                                                                  ↓
                                                            Auto Scaling
                                                         (CPU/Memory > 70%)
```

## Prerequisites

1. **Infrastructure must be deployed first:**
   ```bash
   cd ../../infrastructures
   just apply preprod
   ```

2. **Get your ECR repository URL:**
   ```bash
   cd ../../infrastructures
   terraform output ecr_api1_repository_url
   ```

3. **Update the ECR image URI in `main.tf`** (line 52):
   ```hcl
   container_image = "YOUR_ECR_URL:latest"
   ```

## Deployment Steps

### 1. Update ECR image URI in main.tf

Edit `main.tf` line 52:
```hcl
container_image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-preprod:latest"
```

### 2. Initialize Terraform
```bash
just init
```

### 3. Plan the deployment
```bash
just plan preprod
```

### 4. Apply the deployment
```bash
just apply preprod
```

### 5. Get the API endpoint
```bash
terraform output api_invoke_url
```

## Configuration

All parameters are hardcoded in `main.tf` for explicit configuration:

**📍 ECR Image URI** (Line 52):
```hcl
container_image = "REPLACE_WITH_YOUR_ECR_IMAGE_URI"
```

**Other parameters:**
- `container_port` - 8080 (line 53)
- `task_cpu` - "256" (line 39)
- `task_memory` - "512" (line 40)
- `desired_count` - 2 (line 71)
- `autoscaling_min_capacity` - 2 (line 77)
- `autoscaling_max_capacity` - 10 (line 78)
- `health_check_path` - "/health" (line 17)

## Auto Scaling Triggers

- **Scale UP**: CPU > 70% or Memory > 70% for 2 minutes
- **Scale DOWN**: CPU < 30% or Memory < 30% for 2 minutes
- Cooldown: 60s (up), 300s (down)

## Testing

1. **Health check:**
   ```bash
   curl https://your-api-url/health
   ```

2. **Monitor logs:**
   ```bash
   aws logs tail /ecs/devops2-g4-app-preprod --follow
   ```

3. **Monitor auto scaling:**
   ```bash
   aws ecs describe-services \
     --cluster devops2-g4-api1-cluster-preprod \
     --services devops2-g4-api1-service-preprod
   ```

## Clean Up

```bash
just destroy preprod
```

## Creating More Services (api2, api3, etc.)

Simply copy this folder and update:
1. Service names in all files
2. ECR image URI
3. Container port (if different)
