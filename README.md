# ITRM Assessment 2

This project sets up a complete AWS infrastructure using Terraform, including remote state management, base infrastructure, and service deployments.

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Just (for running recipes) or direct Terraform commands

## How to Run the Project

### 1. Run Remote State

First, set up the remote state backend (S3 bucket and DynamoDB table for state locking).

```bash
cd main/remote-state
just init
just plan prod
just apply prod
```

This creates the S3 bucket `devops2-g4-remote-state-029637202701` and DynamoDB table `remote-state-locking`.

### 2. Run Infrastructure

Next, deploy the base infrastructure (VPC, ALB, security groups, IAM roles, etc.).

```bash
cd ../infrastructures
just init
just plan prod
just apply prod
```

This sets up the shared infrastructure components.

### 3. Run Deployments

Finally, deploy the services (auth, api1, messenger, etc.).

For each deployment:

```bash
cd ../deployments/<service-name>  # e.g., auth, api1, messenger, profile, share, finance
just init
just plan prod
just apply prod
```

Repeat for each service you want to deploy.

## Notes

- Ensure you are in the correct workspace (`prod`) for all operations.
- The deployments depend on the infrastructure outputs, so run infrastructure first.
- Use `terraform output` in the infrastructures directory to verify outputs are available.
- For production, consider using CI/CD pipelines instead of manual runs.
