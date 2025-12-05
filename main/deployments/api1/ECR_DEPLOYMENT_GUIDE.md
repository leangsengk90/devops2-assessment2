# ECR Setup and Docker Image Deployment Guide

## 1. Deploy Infrastructure (Including ECR)

First, deploy the infrastructure which includes the ECR repository:

```bash
cd main/infrastructures
just init
just plan preprod
just apply preprod
```

## 2. Get ECR Repository Information

After applying infrastructure, get your ECR repository URL:

```bash
terraform output ecr_api1_repository_url
```

Example output:
```
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod
```

## 3. Build and Push Docker Image to ECR

### Step 3.1: Authenticate Docker to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 481604401489.dkr.ecr.us-east-1.amazonaws.com
```

### Step 3.2: Build Your Docker Image

Navigate to your application directory (where your Dockerfile is):

```bash
cd /path/to/your/application
docker build -t devops2-g4-api1:latest .
```

### Step 3.3: Tag Your Image

```bash
docker tag devops2-g4-api1:latest 481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest
```

### Step 3.4: Push to ECR

```bash
docker push 481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest
```

## 4. Update Docker Image URI in main.tf

### ⭐ EDIT LOCATION ⭐

Open `main/deployments/api1/main.tf` and update **line 52**:

```hcl
# Before:
container_image = "REPLACE_WITH_YOUR_ECR_IMAGE_URI"

# After (use your actual ECR URL from step 2):
container_image = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest"
```

## 5. Deploy API Service

```bash
cd main/deployments/api1
just init
just plan prod
just apply prod
```

## 6. Update Image (When You Build a New Version)

When you build and push a new image version:

1. Build and push new image to ECR:
   ```bash
   docker build -t devops2-g4-api1:v2 .
   docker tag devops2-g4-api1:v2 481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:v2
   docker push 481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:v2
   ```

2. Update `main.tf` line 52 with the new tag:
   ```hcl
   container_image = "481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:v2"
   ```

3. Re-apply terraform:
   ```bash
   just plan prod
   just apply prod
   ```

## 7. Verify Deployment

After deployment, test your API:

```bash
# Get API Gateway URL
cd main/deployments/api1
terraform output api_invoke_url

# Test the endpoint
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/health
```

## Amazon Inspector

Amazon Inspector will automatically scan your ECR images for vulnerabilities when you push them. Findings will be available in the AWS Console under Amazon Inspector.

If you set `notification_email` in `main/infrastructures/ecr-inspector.tf`, you'll receive email notifications for new findings.

## Notes

- **All configuration is in `main.tf`** - No variables.tf or tfvars files needed
- **ECR image URI**: Edit line 52 in `main.tf` directly
- The ECR repository name follows the pattern: `devops2-g4-api1-{workspace}`
- Images are scanned automatically on push (scan_on_push = true)
- Lifecycle policy keeps only the last 10 images
- Inspector scans ECR images for vulnerabilities

## Configuration Parameters in main.tf

All values are hardcoded in `main.tf`:
- **Line 52**: `container_image` - Your ECR image URI (EDIT THIS!)
- **Line 53**: `container_port` - 8080
- **Line 39**: `task_cpu` - "256"
- **Line 40**: `task_memory` - "512"
- **Line 71**: `desired_count` - 2
- **Line 77**: `autoscaling_min_capacity` - 2
- **Line 78**: `autoscaling_max_capacity` - 10
- **Line 25**: `health_check_path` - "/health"
