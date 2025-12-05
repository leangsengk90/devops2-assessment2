# Infrastructure Summary

## Created Modules

### 1. ECR Module (`modules/ecr/`)
- **Purpose**: Create Amazon ECR repositories for Docker images
- **Features**:
  - Workspace-aware naming
  - Image scanning on push
  - Encryption (AES256 or KMS)
  - Lifecycle policies for image retention
  - Mutable/immutable tag support

### 2. Inspector Module (`modules/inspector/`)
- **Purpose**: Enable Amazon Inspector for security scanning
- **Features**:
  - Scans ECR images and repositories
  - EventBridge integration
  - SNS notifications for findings
  - Email alerts (optional)

## Infrastructure Setup (`main/infrastructures/`)

### New File: `ecr-inspector.tf`
Contains:
- **ECR Repository**: `devops2-g4-api1-{workspace}`
  - Image scanning enabled
  - Keeps last 10 images
  - AES256 encryption
  
- **Amazon Inspector**:
  - Scans ECR images automatically
  - SNS topic for findings (optional email notifications)
  - EventBridge rule to capture findings

### Updated File: `outputs.tf`
Added outputs:
- `ecr_api1_repository_url` - Use this to build your docker tag
- `ecr_api1_repository_arn`
- `ecr_api1_repository_name`
- `inspector_sns_topic_arn`

## Deployment Configuration (`main/deployments/api1/`)

### Variable: `ecr_image_uri` in `variables.tf`
This is where you specify your Docker image URI.

### Usage in `main.tf` (Line 52)
```hcl
module "ecs_service" {
  # ... other configuration ...
  container_image = var.ecr_image_uri  # 👈 Docker image URI goes here
  # ... other configuration ...
}
```

## Complete Deployment Flow

### Phase 1: Deploy Infrastructure (Creates ECR)
```bash
cd main/infrastructures
just init
just plan preprod
just apply preprod
terraform output ecr_api1_repository_url  # Get your ECR URL
```

### Phase 2: Build & Push Docker Image
```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Build
docker build -t devops2-g4-api1:latest .

# Tag
docker tag devops2-g4-api1:latest <ECR_REPOSITORY_URL>:latest

# Push
docker push <ECR_REPOSITORY_URL>:latest
```

### Phase 3: Deploy API Service
```bash
cd main/deployments/api1

# Option 1: Using command line
terraform workspace select preprod || terraform workspace new preprod
terraform plan \
  -var="aws_region=us-east-1" \
  -var="ecr_image_uri=<ECR_REPOSITORY_URL>:latest" \
  -var="container_port=8080" \
  -var="task_cpu=256" \
  -var="task_memory=512" \
  -var="desired_count=2" \
  -var="autoscaling_min_capacity=2" \
  -var="autoscaling_max_capacity=10" \
  -var="health_check_path=/health" \
  -out=../../plans/api1-preprod.plan

terraform apply ../../plans/api1-preprod.plan

# Option 2: Create terraform.tfvars file
# See ECR_DEPLOYMENT_GUIDE.md for details
```

## 📍 WHERE TO INPUT DOCKER IMAGE URI

You have **2 options**:

### Option 1: Command Line (Recommended for CI/CD)
Pass as `-var` flag when running `terraform plan`:
```bash
-var="ecr_image_uri=123456789012.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-preprod:latest"
```

### Option 2: tfvars File (Recommended for Manual Deployment)
Create `main/deployments/api1/terraform.tfvars`:
```hcl
ecr_image_uri = "123456789012.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-preprod:latest"
# ... other variables ...
```

## File Structure

```
main/
├── infrastructures/           # Shared infrastructure (one-time setup)
│   ├── network.tf            # VPC, subnets
│   ├── security-groups.tf    # Security groups for ALB, ECS, VPC Link
│   ├── iam-roles.tf          # IAM roles for ECS
│   ├── cloudwatch.tf         # CloudWatch log groups
│   ├── ecr-inspector.tf      # ✨ NEW: ECR repository + Inspector
│   └── outputs.tf            # Outputs (including ECR URL)
│
└── deployments/
    └── api1/                 # API service deployment
        ├── main.tf           # Service resources (ALB, ECS, API Gateway)
        ├── variables.tf      # Required variables (including ecr_image_uri)
        ├── data.tf           # Remote state data source
        └── ECR_DEPLOYMENT_GUIDE.md  # 📖 Step-by-step guide

modules/
├── ecr/                      # ✨ NEW: ECR module
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
└── inspector/                # ✨ NEW: Inspector module
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

## Amazon Inspector Features

- **Automatic Scanning**: Images are scanned when pushed to ECR
- **Continuous Monitoring**: Repositories are monitored for new vulnerabilities
- **Findings**: Available in AWS Console → Amazon Inspector
- **Notifications**: Optional SNS email alerts for new findings

To enable email notifications, edit `main/infrastructures/ecr-inspector.tf`:
```hcl
module "inspector" {
  # ...
  notification_email = "your-email@example.com"  # Change from null
}
```

## Next Steps

1. ✅ **Deploy infrastructure** → Creates ECR repository
2. ✅ **Build Docker image** → Your application container
3. ✅ **Push to ECR** → Upload image to repository
4. ✅ **Input image URI** → In terraform variables
5. ✅ **Deploy api1** → Creates ECS service with your image
6. ✅ **Test API** → Use API Gateway URL

See `ECR_DEPLOYMENT_GUIDE.md` for detailed instructions!
