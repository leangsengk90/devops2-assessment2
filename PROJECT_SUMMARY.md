# Project Summary: DevOps2 Assessment 2

This is a comprehensive Terraform-based project designed to deploy a scalable, containerized microservices architecture on AWS. It's structured for a DevOps assessment, focusing on infrastructure as code (IaC), remote state management, and modular deployments.

## Overall Purpose

The project sets up a complete AWS environment for running multiple microservices (auth, api1, messenger, profile, share, finance) using Amazon ECS (Elastic Container Service) behind a shared Application Load Balancer (ALB). It includes remote state management for team collaboration, shared infrastructure components, and individual service deployments with auto-scaling and monitoring.

## Key Technologies and Tools

- **Terraform**: Primary IaC tool for defining and provisioning AWS resources.
- **AWS Services**: ECS (clusters and services), ECR (container registries), ALB (load balancing), VPC (networking), CloudWatch (monitoring), IAM (roles), S3 (remote state), DynamoDB (state locking).
- **Just**: Task runner for automating Terraform commands (init, plan, apply) via Justfiles in each directory.
- **Git**: Version control with a main branch.

## Project Structure

The repository is organized into three main directories under `main/`, plus reusable `modules/` and configuration files at the root.

### 1. `modules/` (Reusable Components)

Contains 13 Terraform modules for common AWS resources, each with `main.tf`, `variables.tf`, and `outputs.tf`:

- **vpc**: Virtual Private Cloud setup (subnets, gateways).
- **alb** & **alb-target-group**: Load balancer and target groups for routing traffic.
- **ecs-cluster** & **ecs-service**: ECS cluster and service definitions with auto-scaling.
- **ecr**: Elastic Container Registry for storing Docker images.
- **iam-role**: IAM roles for ECS tasks and execution.
- **security-group**: Security groups for network access control.
- **cloudwatch-log-group** & **cloudwatch-alarm**: Logging and monitoring.
- **dynamodb** & **s3**: Storage services.
- **api-gateway** & **api-gateway-route**: API Gateway for HTTP APIs.
- **inspector**: AWS Inspector for security assessments.

These modules promote reusability and consistency across deployments.

### 2. `main/remote-state/`

Sets up the Terraform backend infrastructure:

- Creates an S3 bucket (`devops2-g4-remote-state`) for storing Terraform state files.
- Creates a DynamoDB table (`remote-state-locking`) for state locking to prevent concurrent modifications.
- Includes `Justfile` for easy execution of Terraform commands.

### 3. `main/infrastructures/`

Deploys shared, foundational AWS resources that services depend on:

- **Network**: VPC with public/private subnets, internet gateway, NAT gateway.
- **Load Balancing**: Shared ALB with HTTP listener.
- **Security**: Security groups for ALB, ECS, VPC Link.
- **IAM**: Roles for ECS task execution and tasks.
- **Monitoring**: CloudWatch log groups.
- **Container Registry**: ECR repositories for each service (auth, api1, messenger, etc.).
- **API Gateway**: Main API Gateway with VPC Link for private integration.
- **Inspector**: SNS topic for security findings.
- Outputs key values (e.g., VPC ID, ALB DNS, role ARNs) for use by deployments.
- Uses local state initially, with S3 backend configured in `versions.tf`.

### 4. `main/deployments/`

Contains individual service deployments, each in its own subdirectory (auth, api1, messenger, profile, share, finance):

- Each deployment includes:
  - `main.tf`: Defines ECS service, ALB target group, API Gateway route, and other service-specific resources.
  - `variables.tf`, `providers.tf`, `versions.tf`: Standard Terraform files.
  - `data.tf`: References remote state from `infrastructures` to access shared outputs.
  - `outputs.tf`: Exposes service-specific outputs (e.g., ALB DNS, API endpoint).
  - `Justfile`: Automation for Terraform commands.
  - Local state files under `terraform.tfstate.d/prod/` (for prod workspace).
- Services are containerized, deployed to ECS with auto-scaling, health checks, and logging.
- Integrates with shared ALB and API Gateway.

### Root-Level Files

- `README.md`: Project documentation (recently added with run instructions).
- `variables/global.tfvars`: Global variable definitions.
- `COST_ANALYSIS.md` & `INFRASTRUCTURE_SUMMARY.md`: Documentation on costs and infrastructure design.
- `diagram.txt`: Likely a text-based architecture diagram.
- `.gitignore`: Excludes sensitive files like state backups.

## Architecture and Workflow

- **Modular Design**: Modules allow easy reuse; deployments reference shared infrastructure via remote state.
- **State Management**: Remote state in S3 ensures team collaboration; local state used during development.
- **Workspaces**: Supports multiple environments (e.g., prod) via Terraform workspaces.
- **Deployment Flow**: 1) Set up remote state, 2) Deploy shared infrastructure, 3) Deploy individual services.
- **Scalability**: ECS services include auto-scaling based on CPU/memory; ALB distributes traffic.
- **Security**: IAM roles with least privilege, security groups, VPC isolation.
- **Monitoring**: CloudWatch logs and alarms for operational visibility.

## Key Features

- **Microservices**: Each service (auth, api1, etc.) is independently deployable.
- **Containerization**: Uses ECR for image storage; ECS for orchestration.
- **API Integration**: API Gateway routes requests to services via VPC Link.
- **Health Checks**: ALB and ECS health checks ensure reliability.
- **Automation**: Justfiles simplify common Terraform operations.

This project demonstrates best practices for AWS infrastructure deployment with Terraform, suitable for production use with CI/CD integration. Total files: ~254, with a focus on maintainability and scalability. If you need details on specific files or modifications, let me know!
