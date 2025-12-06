# Infrastructure Summary

## Architecture Overview

**Region:** us-east-1  
**Environment:** Production  
**Microservices:** 6 services (api1, auth, profile, messenger, finance, share)  
**API Gateway:** 1 shared HTTP API with path-based routing  
**Load Balancer:** 1 shared ALB with header-based routing ✅ **Optimized**

## Key Features

✅ **Cost Optimized** - Consolidated from 6 ALBs to 1 shared ALB (saves $352/month)  
✅ **Scalable** - Auto-scaling from 2-10 tasks per service  
✅ **Secure** - Private ALB, ECR image scanning, VPC isolation  
✅ **Observable** - CloudWatch Container Insights, centralized logging  
✅ **Resilient** - Multi-AZ deployment, health checks, auto-recovery

---

## Created Modules

### 1. VPC Module (`modules/vpc/`)

- **Purpose**: Create VPC with public and private subnets
- **Features**:
  - Multi-AZ deployment
  - Public subnets for NAT Gateways
  - Private subnets for ECS tasks
  - Internet Gateway and route tables

### 2. Security Group Module (`modules/security-group/`)

- **Purpose**: Network security and access control
- **Features**:
  - ALB security group (allows VPC Link traffic)
  - ECS security group (allows ALB traffic only)
  - VPC Link security group (HTTPS from internet)

### 3. ALB Module (`modules/alb/`)

- **Purpose**: Application Load Balancer for HTTP traffic
- **Features**:
  - HTTP listener on port 80
  - Target group with health checks
  - Multi-AZ distribution
  - Connection draining support

### 4. ALB Target Group Module (`modules/alb-target-group/`) ✅ **NEW**

- **Purpose**: Create target groups and listener rules for shared ALB
- **Features**:
  - Header-based routing using `X-Service-Name`
  - Configurable health checks
  - Support for different container ports
  - Priority-based listener rules

### 5. ECS Cluster Module (`modules/ecs-cluster/`)

- **Purpose**: Create ECS clusters for container orchestration
- **Features**:
  - Container Insights enabled
  - CloudWatch log groups
  - Workspace-aware naming
  - Performance monitoring

### 6. ECS Service Module (`modules/ecs-service/`)

- **Purpose**: Deploy containerized applications
- **Features**:
  - Fargate launch type (serverless)
  - Auto-scaling (CPU/Memory based)
  - Health checks and load balancer integration
  - CloudWatch alarms
  - Rolling deployments

### 7. API Gateway Route Module (`modules/api-gateway-route/`) ✅ **NEW**

- **Purpose**: Create API Gateway routes with path rewriting
- **Features**:
  - Path-based routing (e.g., `/finance`, `/auth`)
  - Automatic path prefix stripping
  - Custom header injection (`X-Service-Name`)
  - VPC Link integration
  - HTTP proxy integration

### 8. ECR Module (`modules/ecr/`)

- **Purpose**: Container image registry
- **Features**:
  - Workspace-aware naming
  - Image scanning on push
  - Encryption (AES256 or KMS)
  - Lifecycle policies for image retention
  - Mutable/immutable tag support

### 9. Inspector Module (`modules/inspector/`)

- **Purpose**: Security vulnerability scanning
- **Features**:
  - Scans ECR images and repositories
  - EventBridge integration
  - SNS notifications for findings
  - Email alerts (optional)

### 10. CloudWatch Modules

- **Log Group Module** (`modules/cloudwatch-log-group/`): Centralized logging
- **Alarm Module** (`modules/cloudwatch-alarm/`): Auto-scaling triggers

### 11. IAM Role Module (`modules/iam-role/`)

- **Purpose**: IAM roles for ECS tasks
- **Features**:
  - Task execution role (pull images, write logs)
  - Task role (application permissions)

---

## Infrastructure Components (`main/infrastructures/`)

### Core Network (`network.tf`)

- VPC (10.0.0.0/16)
- Private subnets (Multi-AZ)
- Public subnets (Multi-AZ)
- NAT Gateways (2 for HA)
- Internet Gateway
- Route tables

### Security (`security-groups.tf`)

- ALB security group (port 80 from VPC Link)
- ECS security group (allows ALB traffic)
- VPC Link security group (port 443 from internet)

### IAM Roles (`iam-roles.tf`)

- ECS Task Execution Role
  - Pull ECR images
  - Write CloudWatch logs
- ECS Task Role
  - Application-level permissions

### CloudWatch (`cloudwatch.tf`)

- Centralized log group: `/aws/ecs/devops2-g4-app`
- API Gateway logs: `/aws/apigateway/devops2-g4-main-prod`
- Retention: 7 days

### Shared API Gateway (`api-gateway.tf`) ✅ **NEW**

- HTTP API Gateway
- VPC Link to private ALB
- $default stage with auto-deploy
- CORS enabled
- Throttling: 5000 burst, 10000/sec rate

### Shared ALB (`alb.tf`) ✅ **NEW**

- Internal Application Load Balancer
- HTTP listener on port 80
- Default action: 404 (service not found)
- Multi-AZ distribution
- Security: Accepts traffic from VPC Link only

### ECR Repositories (`ecr-inspector.tf`)

6 repositories with Amazon Inspector scanning:

- `devops2-g4-api1-prod`
- `devops2-g4-auth-prod`
- `devops2-g4-profile-prod`
- `devops2-g4-messenger-prod`
- `devops2-g4-finance-prod`
- `devops2-g4-share-prod`

### Outputs (`outputs.tf`)

Key infrastructure outputs:

- VPC and subnet IDs
- Security group IDs
- IAM role ARNs
- **Shared ALB ARN and DNS name** ✅
- **Shared ALB listener ARN** ✅
- **API Gateway ID and endpoint** ✅
- **VPC Link ID** ✅
- ECR repository URLs (all 6 services)

---

## Service Deployments (`main/deployments/`)

### Architecture Pattern (All 6 Services)

Each service follows the same pattern:

```
main/deployments/{service}/
├── main.tf              # Service infrastructure
├── variables.tf         # Service variables
├── outputs.tf           # Service outputs
├── data.tf             # Remote state reference
├── providers.tf        # Terraform providers
├── versions.tf         # Terraform version constraints
└── Justfile           # Deployment commands
```

### Service Details

| Service       | Container Port | Listener Priority | Path Patterns                | Health Check |
| ------------- | -------------- | ----------------- | ---------------------------- | ------------ |
| **api1**      | 80             | 100               | `/api1`, `/api1/*`           | `/`          |
| **auth**      | 3000           | 200               | `/auth`, `/auth/*`           | `/`          |
| **profile**   | 3001           | 300               | `/profile`, `/profile/*`     | `/`          |
| **messenger** | 3002           | 400               | `/messenger`, `/messenger/*` | `/`          |
| **finance**   | 8080           | 500               | `/finance`, `/finance/*`     | `/api/hello` |
| **share**     | 3004           | 600               | `/share`, `/share/*`         | `/`          |

### Common Service Components

Each service includes:

1. **ALB Target Group** (via `alb-target-group` module)

   - Header-based routing
   - Health checks
   - Listener rule with unique priority

2. **ECS Cluster** (via `ecs-cluster` module)

   - Container Insights enabled
   - CloudWatch logging

3. **ECS Service** (via `ecs-service` module)

   - Fargate launch type
   - Auto-scaling: 2-10 tasks
   - CPU threshold: 30-70%
   - Memory threshold: 30-70%

4. **API Gateway Route** (via `api-gateway-route` module)
   - Path-based routing
   - Path rewriting (strips service prefix)
   - Header injection for ALB routing

---

## Traffic Flow Architecture

### Request Flow Example: `/finance/api/hello`

```
1. Client
   ↓ HTTPS
   GET https://xxxxx.execute-api.us-east-1.amazonaws.com/finance/api/hello

2. API Gateway (HTTP API)
   ↓ Matches route: ANY /finance/{proxy+}
   ↓ Strips prefix: /api/hello
   ↓ Adds header: X-Service-Name: devops2-g4-finance

3. VPC Link
   ↓ Connects to private VPC

4. Shared ALB
   ↓ Receives: /api/hello + header
   ↓ Listener rule matches: X-Service-Name = devops2-g4-finance
   ↓ Routes to: finance target group

5. Finance Target Group
   ↓ Forwards to healthy task on port 8080

6. Finance ECS Task (Container)
   ↓ Receives: /api/hello
   ↓ Processes request

7. Response
   ↓ Returns through same path
   ← Client receives response
```

### Key Routing Features

✅ **Path Rewriting**: API Gateway strips service prefix before forwarding  
✅ **Header-Based Routing**: ALB uses `X-Service-Name` header to route  
✅ **Service Isolation**: Each service has dedicated target group  
✅ **Port Flexibility**: Services can use different container ports  
✅ **Clean APIs**: Containers receive clean paths without service prefix

---

## Complete Deployment Flow

### Phase 1: Deploy Shared Infrastructure

Creates VPC, security groups, IAM roles, shared ALB, API Gateway, ECR repositories.

```bash
cd main/infrastructures

# Initialize Terraform
terraform init

# Select workspace
terraform workspace select prod || terraform workspace new prod

# Plan changes
terraform plan -var-file=../../variables/global.tfvars -out=../../plans/infrastructure-prod.plan

# Apply infrastructure
terraform apply ../../plans/infrastructure-prod.plan

# Get outputs
terraform output
```

**Key Outputs:**

- `shared_alb_dns_name` - Internal ALB DNS
- `shared_alb_listener_arn` - For service deployments
- `api_gateway_endpoint` - Public API endpoint
- `ecr_*_repository_url` - Docker image URLs for each service

---

### Phase 2: Build & Push Docker Images

For each service, build and push container image to ECR.

#### Example: Finance Service

```bash
# Get ECR repository URL
cd main/infrastructures
ECR_URL=$(terraform output -raw ecr_finance_repository_url)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# Build Docker image
cd /path/to/finance-app
docker build -t devops2-g4-finance:latest .

# Tag for ECR
docker tag devops2-g4-finance:latest ${ECR_URL}:latest

# Push to ECR
docker push ${ECR_URL}:latest
```

**Repeat for all 6 services:**

- api1 (nginx:alpine or custom app on port 80)
- auth (custom app on port 3000)
- profile (custom app on port 3001)
- messenger (custom app on port 3002)
- finance (custom app on port 8080)
- share (custom app on port 3004)

---

### Phase 3: Deploy Services

Deploy each microservice with its ECS cluster, service, and routing configuration.

#### Example: Deploy Finance Service

```bash
cd main/deployments/finance

# Select workspace
terraform workspace select prod || terraform workspace new prod

# Plan deployment
terraform plan \
  -var-file=../../../variables/global.tfvars \
  -out=../../../plans/finance-prod.plan

# Apply deployment
terraform apply ../../../plans/finance-prod.plan

# Get service endpoint
terraform output api_invoke_url
```

**Deploy order (recommended):**

1. api1 (test basic functionality)
2. auth (authentication service)
3. profile, messenger, finance, share (in any order)

---

### Phase 4: Verify Deployment

#### Check ALB Target Groups

```bash
# List all target groups
aws elbv2 describe-target-groups \
  --query 'TargetGroups[?contains(TargetGroupName, `devops2-g4`)].TargetGroupName'

# Check health of targets
aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN>
```

#### Test API Endpoints

```bash
# Get API Gateway endpoint
cd main/infrastructures
API_ENDPOINT=$(terraform output -raw api_gateway_endpoint)

# Test each service
curl ${API_ENDPOINT}/api1
curl ${API_ENDPOINT}/auth
curl ${API_ENDPOINT}/profile
curl ${API_ENDPOINT}/messenger
curl ${API_ENDPOINT}/finance/api/hello
curl ${API_ENDPOINT}/share
```

#### Monitor Logs

```bash
# View ECS service logs
aws logs tail /aws/ecs/devops2-g4-app --follow

# View API Gateway logs
aws logs tail /aws/apigateway/devops2-g4-main-prod --follow
```

---

## Management Commands

### Using Justfile

Each deployment has a `Justfile` with common commands:

```bash
cd main/deployments/{service}

# Initialize Terraform
just init

# Plan changes for prod
just plan prod

# Apply changes for prod
just apply prod

# Destroy resources
just destroy prod

# Format Terraform files
just fmt

# Validate configuration
just validate
```

### Manual Terraform Commands

```bash
# Initialize
terraform init

# Select workspace
terraform workspace select prod

# Plan
terraform plan -var-file=../../../variables/global.tfvars

# Apply
terraform apply -var-file=../../../variables/global.tfvars

# Destroy
terraform destroy -var-file=../../../variables/global.tfvars
```

---

## Monitoring & Observability

### CloudWatch Container Insights

Enabled for all ECS clusters, provides:

- CPU and memory utilization
- Network metrics
- Container performance metrics

**View in AWS Console:**  
CloudWatch → Container Insights → ECS Clusters

### CloudWatch Logs

Centralized logging:

- ECS task logs: `/aws/ecs/devops2-g4-app`
- API Gateway logs: `/aws/apigateway/devops2-g4-main-prod`
- Container Insights: `/aws/ecs/containerinsights/{cluster}/performance`

### CloudWatch Alarms

Each service has 4 auto-scaling alarms:

- `{service}-cpu-high-prod` - Scale up when CPU > 70%
- `{service}-cpu-low-prod` - Scale down when CPU < 30%
- `{service}-memory-high-prod` - Scale up when Memory > 70%
- `{service}-memory-low-prod` - Scale down when Memory < 30%

### Amazon Inspector

Automatic vulnerability scanning:

- Scans container images on push
- Continuous monitoring for CVEs
- Findings available in Inspector console

**View Findings:**  
AWS Console → Amazon Inspector → Findings

---

## Security Features

### Network Security

✅ **Private ALB** - Not exposed to internet  
✅ **VPC Isolation** - ECS tasks in private subnets  
✅ **Security Groups** - Least privilege access  
✅ **NAT Gateway** - Outbound internet for tasks

### Access Control

✅ **IAM Roles** - Task execution and task roles  
✅ **ECR Image Scanning** - Amazon Inspector  
✅ **Encrypted Logs** - CloudWatch encryption  
✅ **VPC Link** - Secure API Gateway to VPC connection

### Best Practices

✅ **Multi-AZ Deployment** - High availability  
✅ **Health Checks** - Automatic recovery  
✅ **Auto-scaling** - Handle traffic spikes  
✅ **Container Insights** - Performance monitoring  
✅ **Centralized Logging** - Audit trail

---

## Cost Optimization

### Implemented Optimizations

✅ **Shared ALB** - Saves $352.52/month (79% reduction)  
✅ **Path-based Routing** - Efficient resource utilization  
✅ **Auto-scaling** - Pay only for what you use  
✅ **Fargate** - No EC2 management overhead

### Current Monthly Cost (Average Load)

```
ECS Fargate (30 tasks):      $1,081.76
Shared ALB:                  $96.43     ✅ Optimized
API Gateway:                 $9.00
NAT Gateway:                 $88.20
VPC Link:                    $7.30
ECR:                         $1.00
CloudWatch:                  $117.55
Inspector:                   $2.70
Data Transfer:               $2.00
─────────────────────────────────────
TOTAL:                       $1,405.94/month
```

**Achieved Savings:** $352.52/month from ALB consolidation

See `COST_ANALYSIS.md` for detailed cost breakdown and optimization strategies.

---

## File Structure

---

## File Structure

```
devops2-assessment2/
├── main/
│   ├── infrastructures/              # Shared infrastructure (deploy once)
│   │   ├── network.tf               # VPC, subnets, NAT gateways
│   │   ├── security-groups.tf       # Security groups
│   │   ├── iam-roles.tf             # IAM roles for ECS
│   │   ├── cloudwatch.tf            # Log groups
│   │   ├── api-gateway.tf           # ✅ Shared API Gateway + VPC Link
│   │   ├── alb.tf                   # ✅ Shared ALB
│   │   ├── ecr-inspector.tf         # ECR repositories + Inspector
│   │   ├── outputs.tf               # Infrastructure outputs
│   │   ├── providers.tf             # AWS provider config
│   │   ├── versions.tf              # Terraform version
│   │   ├── variables.tf             # Infrastructure variables
│   │   ├── data.tf                  # Remote state backend
│   │   └── Justfile                 # Deployment commands
│   │
│   ├── deployments/
│   │   ├── api1/                    # API1 service
│   │   │   ├── main.tf              # Service resources
│   │   │   ├── variables.tf         # Service variables
│   │   │   ├── outputs.tf           # Service outputs
│   │   │   ├── data.tf              # Remote state reference
│   │   │   ├── providers.tf         # Provider config
│   │   │   ├── versions.tf          # Terraform version
│   │   │   └── Justfile             # Deployment commands
│   │   │
│   │   ├── auth/                    # Auth service
│   │   ├── profile/                 # Profile service
│   │   ├── messenger/               # Messenger service
│   │   ├── finance/                 # Finance service
│   │   └── share/                   # Share service
│   │       └── (same structure as api1)
│   │
│   └── remote-state/                # Terraform state backend
│       ├── s3.tf                    # S3 bucket for state
│       ├── dynamodb.tf              # DynamoDB for state locking
│       └── ...
│
├── modules/                         # Reusable Terraform modules
│   ├── vpc/                         # VPC module
│   ├── security-group/              # Security group module
│   ├── alb/                         # ALB module
│   ├── alb-target-group/            # ✅ Target group + listener rule module
│   ├── ecs-cluster/                 # ECS cluster module
│   ├── ecs-service/                 # ECS service module
│   ├── api-gateway-route/           # ✅ API Gateway route module
│   ├── ecr/                         # ECR repository module
│   ├── inspector/                   # Amazon Inspector module
│   ├── cloudwatch-log-group/        # Log group module
│   ├── cloudwatch-alarm/            # CloudWatch alarm module
│   └── iam-role/                    # IAM role module
│
├── variables/                       # Variable files
│   ├── global.tfvars                # Global variables
│   ├── preprod.tfvars               # Pre-production variables
│   └── prod.tfvars                  # Production variables
│
├── plans/                           # Terraform plan outputs
│   ├── infrastructure-prod.plan
│   ├── api1-prod.plan
│   ├── auth-prod.plan
│   └── ...
│
├── diagram.txt                      # Architecture diagram
├── COST_ANALYSIS.md                 # ✅ Cost breakdown and optimization
├── INFRASTRUCTURE_SUMMARY.md        # This file
└── README.md                        # Project overview
```

---

## Quick Reference

### Important URLs

- **API Gateway Endpoint**: `https://{api-id}.execute-api.us-east-1.amazonaws.com`
- **Service Paths**:
  - `/api1` → API1 service
  - `/auth` → Auth service
  - `/profile` → Profile service
  - `/messenger` → Messenger service
  - `/finance` → Finance service
  - `/share` → Share service

### Important ARNs/IDs (from infrastructure outputs)

```bash
# Get all infrastructure outputs
cd main/infrastructures
terraform output

# Key outputs:
shared_alb_arn                 # ALB ARN
shared_alb_dns_name            # Internal ALB DNS
shared_alb_listener_arn        # For service deployments
api_gateway_id                 # API Gateway ID
api_gateway_endpoint           # Public API endpoint
vpc_link_id                    # VPC Link ID
ecr_*_repository_url           # ECR URLs for each service
```

### Container Image URIs

```
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-api1-prod:latest
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-auth-prod:latest
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-profile-prod:latest
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-messenger-prod:latest
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-finance-prod:latest
481604401489.dkr.ecr.us-east-1.amazonaws.com/devops2-g4-share-prod:latest
```

---

## Troubleshooting

### Service Not Found (404)

**Symptom**: API Gateway returns "Service not found"

**Causes & Solutions**:

1. ✅ **Service not deployed** → Deploy the service deployment
2. ✅ **Route not created** → Check `terraform output` in service deployment
3. ✅ **ALB listener rule missing** → Verify listener rule in AWS Console

### Health Check Failing

**Symptom**: Targets unhealthy in target group

**Causes & Solutions**:

1. ✅ **Container port mismatch** → Ensure target group port matches container port
2. ✅ **Health check path wrong** → Verify health check endpoint exists
3. ✅ **Container not starting** → Check CloudWatch logs for errors
4. ✅ **Security group blocks traffic** → Verify ECS SG allows ALB traffic

### Container Cannot Pull Image

**Symptom**: ECS task fails with "CannotPullContainerError"

**Causes & Solutions**:

1. ✅ **Image doesn't exist** → Push image to ECR first
2. ✅ **Wrong image URI** → Check ECR repository URL
3. ✅ **IAM permissions** → Verify task execution role has ECR permissions
4. ✅ **No internet access** → Check NAT Gateway and route tables

### Auto-scaling Not Working

**Symptom**: Service doesn't scale up/down

**Causes & Solutions**:

1. ✅ **Alarms not configured** → Check CloudWatch alarms exist
2. ✅ **Thresholds not met** → Review CloudWatch metrics
3. ✅ **Cooldown period** → Wait for cooldown (300 seconds)
4. ✅ **Max capacity reached** → Check max capacity setting

---

## Next Steps

### 1. Initial Deployment

- [ ] Deploy shared infrastructure (`main/infrastructures`)
- [ ] Build and push Docker images to ECR
- [ ] Deploy all 6 services
- [ ] Test API endpoints
- [ ] Verify health checks

### 2. Production Readiness

- [ ] Set up CloudWatch dashboards
- [ ] Configure SNS alerts for alarms
- [ ] Enable Amazon Inspector email notifications
- [ ] Document API specifications
- [ ] Create runbooks for common issues

### 3. Optimization

- [ ] Monitor costs in AWS Cost Explorer
- [ ] Analyze Container Insights metrics
- [ ] Consider Fargate Spot (Phase 2 optimization)
- [ ] Add VPC Endpoints for ECR (Phase 3 optimization)
- [ ] Right-size task definitions (Phase 4 optimization)

### 4. CI/CD Integration

- [ ] Automate Docker image builds
- [ ] Automate ECR pushes
- [ ] Automate Terraform deployments
- [ ] Set up blue-green deployments
- [ ] Implement automated testing

---

## Additional Resources

- **Architecture Diagram**: See `diagram.txt` for visual representation
- **Cost Analysis**: See `COST_ANALYSIS.md` for detailed cost breakdown
- **AWS Documentation**:
  - [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
  - [API Gateway HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)
  - [ALB Listener Rules](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-update-rules.html)
  - [Fargate Pricing](https://aws.amazon.com/fargate/pricing/)

---

## Document Information

**Last Updated**: December 6, 2025  
**Architecture Version**: Shared ALB (Optimized)  
**Environment**: Production  
**Region**: us-east-1

**Key Changes from Previous Version**:

- ✅ Consolidated 6 ALBs → 1 shared ALB
- ✅ Implemented header-based routing at ALB
- ✅ Added path rewriting at API Gateway
- ✅ Achieved $352.52/month cost savings (79% ALB cost reduction)
