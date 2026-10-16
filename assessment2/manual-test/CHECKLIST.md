# Manual console build checklist

This checklist builds, by hand in the AWS console, exactly what one Terraform rebuild creates: **140 resources** across 7 sections. Every name and value below is copied from the Terraform code, so `compare.py` can check your build against the Terraform one.

**Rules for every run**
- **Region:** `ap-southeast-2` (Sydney).
- **Same order every time:** sections 0 → 7. Don't skip ahead.
- **Timer:** start it at your **first click that creates something**. Stop it when all 5 service URLs return HTTP 200 (step 7.3).
- **Tags:** where a step lists tags, add them. Missing tags count as differences in the comparison.
  - `Environment = prod` on everything.
  - `Name` and `Service` as listed in each step.
- **Mistakes:** if you fix or recreate something, add 1 to the "mistakes" count on the recording sheet and write a short note.
- **The ECR repositories and images are kept from Terraform.** Do not create them.

Tick each box as you go. If you print it, leave the count column blank and fill it in.

---

## 0. Terraform state backend (7 resources)

**0.1 S3 bucket** (S3 → Create bucket): 6 resources

- [ ] **Name:** `devops2-g4-remote-state-029637202701`
- [ ] **Block all public access:** ON (all 4 boxes)
- [ ] **Bucket Versioning:** Enable
- [ ] **Default encryption:** SSE-S3 (AES256); Bucket Key **disabled**
- [ ] **Tags:** `Name = devops2-g4-remote-state-029637202701`, `Environment = prod`, `Service = devops2-g4-remote-state-029637202701`
- [ ] **Permissions → CORS:** paste:

  ```json
  [{"AllowedHeaders":["*"],"AllowedMethods":["GET","POST","PUT","DELETE"],"AllowedOrigins":["*"],"MaxAgeSeconds":3000}]
  ```

- [ ] **Management → Lifecycle rule 1:** `cleanup-old-versions`, whole bucket, permanently delete noncurrent versions after **30** days
- [ ] **Management → Lifecycle rule 2:** `expire-temp-files`, prefix `temp/`, expire current versions after **7** days

**0.2 DynamoDB table** (DynamoDB → Create table): 1 resource

- [ ] **Table name:** `remote-state-locking`
- [ ] **Partition key:** `LockID` (String)
- [ ] **Capacity:** On-demand
- [ ] **Encryption:** owned by DynamoDB (default)
- [ ] **TTL:** after creation, Additional settings → Time to Live → attribute `TimeToExist`, enable
- [ ] **Tags:** `Environment = prod`, `Service = remote-state-locking`

---

## 1. Network (17 resources)

Don't use the VPC wizard's extras. Create each item so the names and CIDRs match exactly.

| ✓ | Resource | Name tag | Settings |
|---|---|---|---|
| ☐ | VPC | `devops2-g4-app-vpc-prod` | CIDR `10.0.0.0/16`; DNS hostnames **on**; DNS resolution **on** |
| ☐ | Subnet | `devops2-g4-app-public-subnet-ap-southeast-2a-prod` | `10.0.1.0/24`, AZ `ap-southeast-2a`; then *Edit subnet settings* → auto-assign public IPv4 **on** |
| ☐ | Subnet | `devops2-g4-app-public-subnet-ap-southeast-2b-prod` | `10.0.2.0/24`, AZ `ap-southeast-2b`; auto-assign public IPv4 **on** |
| ☐ | Subnet | `devops2-g4-app-private-subnet-ap-southeast-2a-prod` | `10.0.11.0/24`, AZ `ap-southeast-2a` |
| ☐ | Subnet | `devops2-g4-app-private-subnet-ap-southeast-2b-prod` | `10.0.12.0/24`, AZ `ap-southeast-2b` |
| ☐ | Internet gateway | `devops2-g4-app-igw-prod` | Attach to the VPC |
| ☐ | Elastic IP | `devops2-g4-app-nat-eip-ap-southeast-2a-prod` | Allocate |
| ☐ | Elastic IP | `devops2-g4-app-nat-eip-ap-southeast-2b-prod` | Allocate |
| ☐ | NAT gateway | `devops2-g4-app-nat-gateway-ap-southeast-2a-prod` | Public subnet **2a**, EIP 2a, connectivity Public |
| ☐ | NAT gateway | `devops2-g4-app-nat-gateway-ap-southeast-2b-prod` | Public subnet **2b**, EIP 2b |
| ☐ | Route table | `devops2-g4-app-public-rt-prod` | Route `0.0.0.0/0` → internet gateway |
| ☐ | Association | — | Public RT ↔ public subnet 2a |
| ☐ | Association | — | Public RT ↔ public subnet 2b |
| ☐ | Route table | `devops2-g4-app-private-rt-ap-southeast-2a-prod` | Route `0.0.0.0/0` → NAT gateway **2a** |
| ☐ | Association | — | Private RT 2a ↔ private subnet 2a |
| ☐ | Route table | `devops2-g4-app-private-rt-ap-southeast-2b-prod` | Route `0.0.0.0/0` → NAT gateway **2b** |
| ☐ | Association | — | Private RT 2b ↔ private subnet 2b |

Tags on all of the above: `Environment = prod`, `Service = devops2-g4-app`.

---

## 2. Security groups (3 groups + 7 rules = 10 resources)

Create the three groups first with **no rules**, delete the default "allow all outbound" rule from each, then add the rules below. Each group references the others.

| ✓ | Group name (and Name tag) | Description |
|---|---|---|
| ☐ | `devops2-g4-alb-sg-prod` | Security group for Application Load Balancer |
| ☐ | `devops2-g4-ecs-sg-prod` | Security group for ECS Fargate tasks |
| ☐ | `devops2-g4-vpclink-sg-prod` | Security group for API Gateway VPC Link |

| ✓ | Group | Direction | Protocol / ports | Source or destination | Rule description |
|---|---|---|---|---|---|
| ☐ | alb-sg | Inbound | TCP 80 | `10.0.0.0/16` | Allow HTTP from VPC Link |
| ☐ | alb-sg | Inbound | TCP 443 | `10.0.0.0/16` | Allow HTTPS from VPC Link |
| ☐ | alb-sg | Outbound | TCP 0–65535 | ecs-sg | Allow all outbound to ECS tasks |
| ☐ | ecs-sg | Inbound | TCP 0–65535 | alb-sg | Allow traffic from ALB |
| ☐ | ecs-sg | Outbound | All traffic | `0.0.0.0/0` | Allow all outbound traffic |
| ☐ | vpclink-sg | Inbound | TCP 443 | `0.0.0.0/0` | Allow HTTPS from anywhere |
| ☐ | vpclink-sg | Outbound | TCP 0–65535 | alb-sg | Allow traffic to ALB |

Tags on the groups: `Environment = prod`, `Service = devops2-g4-app`.

---

## 3. IAM roles (5 resources)

**3.1 Role `devops2-g4-ecs-task-execution-role-prod`** (IAM → Roles → Create role)

- [ ] **Trusted entity:** AWS service → Elastic Container Service → **Elastic Container Service Task**
- [ ] **Attach managed policy:** `AmazonECSTaskExecutionRolePolicy`
- [ ] **Add inline policy:** named `devops2-g4-ecs-task-execution-role-inline-policy-prod`, with this JSON:

  ```json
  {"Version":"2012-10-17","Statement":[
   {"Effect":"Allow","Action":["ecr:GetAuthorizationToken","ecr:BatchCheckLayerAvailability","ecr:GetDownloadUrlForLayer","ecr:BatchGetImage"],"Resource":"*"},
   {"Effect":"Allow","Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],"Resource":"arn:aws:logs:ap-southeast-2:*:log-group:/ecs/*"}]}
  ```

- [ ] **Tags:** `Environment = prod`, `Service = devops2-g4-app`

**3.2 Role `devops2-g4-ecs-task-role-prod`**

- [ ] **Trusted entity:** same as above (ECS Task)
- [ ] **Add inline policy:** named `devops2-g4-ecs-task-role-inline-policy-prod`:

  ```json
  {"Version":"2012-10-17","Statement":[
   {"Effect":"Allow","Action":["s3:GetObject","s3:PutObject","s3:ListBucket"],"Resource":["arn:aws:s3:::devops2-g4-*","arn:aws:s3:::devops2-g4-*/*"]},
   {"Effect":"Allow","Action":["dynamodb:GetItem","dynamodb:PutItem","dynamodb:UpdateItem","dynamodb:Query","dynamodb:Scan"],"Resource":"arn:aws:dynamodb:ap-southeast-2:*:table/devops2-g4-*"},
   {"Effect":"Allow","Action":["ssm:GetParameter","ssm:GetParameters"],"Resource":"arn:aws:ssm:ap-southeast-2:*:parameter/devops2-g4/*"}]}
  ```

- [ ] **Tags:** `Environment = prod`, `Service = devops2-g4-app`

---

## 4. Logs, alerts, load balancer and API Gateway (11 resources)

| ✓ | Console | Resource | Settings |
|---|---|---|---|
| ☐ | CloudWatch → Log groups | `/ecs/devops2-g4-app-prod` | Retention 7 days; tags `Environment = prod`, `Service = devops2-g4-app` |
| ☐ | CloudWatch → Log groups | `/aws/apigateway/devops2-g4-main-prod` | Retention 7 days; tags `Environment = prod`, `Service = devops2-g4-main` |
| ☐ | SNS → Topics | `devops2-g4-app-inspector-findings-prod` | Standard; access policy: allow `events.amazonaws.com` to `sns:Publish` to this topic |
| ☐ | EventBridge → Rules | `devops2-g4-app-inspector-findings-prod` | Description "Capture Inspector findings"; pattern `{"source":["aws.inspector2"],"detail-type":["Inspector2 Finding"]}` |
| ☐ | (same rule) | Target | SNS topic above (counts as its own resource) |
| ☐ | (SNS topic) | Topic policy | Counts as its own resource |
| ☐ | EC2 → Load balancers | `devops2-g4-shared-alb-prod` | Application, **Internal**, IPv4, the VPC, **both private subnets**, security group `alb-sg` only. HTTP/2 on, deletion protection off. Tags `Name = devops2-g4-shared-alb-prod`, `Environment = prod`, `Service = devops2-g4-shared` |
| ☐ | (ALB) Listener | HTTP : 80 | Default action **Return fixed response**: 404, `text/plain`, body `Service not found` |
| ☐ | API Gateway → VPC links (for HTTP APIs) | `devops2-g4-vpclink-prod` | Both private subnets; security group `vpclink-sg` |
| ☐ | API Gateway → Create HTTP API | `devops2-g4-main-prod` | Description "Main API Gateway for all microservices"; no integrations yet |
| ☐ | (API) CORS | — | Origins `*`; methods GET, POST, PUT, DELETE, OPTIONS; headers `*`; max age 300 |
| ☐ | (API) Stage | `$default` | Auto-deploy on; throttling burst 5000, rate 10000; access logging to `/aws/apigateway/devops2-g4-main-prod`, JSON format with requestId, ip, requestTime, httpMethod, routeKey, status, protocol, responseLength |

The NAT gateways and load balancer take a few minutes to become active. Carry on with the next steps while they start.

---

## 5. Services: repeat for each of the 5 services (18 resources each = 90)

Use this table for the values that change per service. `<svc>` means the service name (e.g. `auth`).

| Service | Container name | Port | Health check path | Listener priority | API route |
|---|---|---|---|---|---|
| auth | `auth-app` | 3000 | `/` | 200 | `/auth` |
| profile | `profile-app` | 3001 | `/` | 300 | `/profile` |
| messenger | `messenger-app` | 3002 | `/` | 400 | `/messenger` |
| finance | `finance-app` | 8080 | `/api/hello` | 500 | `/finance` |
| share | `share-app` | 3004 | `/` | 600 | `/share` |

**Tags for every resource in this section:** `Environment = prod`, `Service = devops2-g4-<svc>`.

**5.1 Target group** (EC2 → Target groups): 1 resource

- [ ] **Type:** IP addresses
- [ ] **Name:** `devops2-g4-<svc>-tg-prod`
- [ ] **Protocol / port:** HTTP, the service's port
- [ ] **VPC:** the VPC
- [ ] **Health check:** HTTP, the service's path. Advanced settings: healthy 2, unhealthy 3, timeout 5, interval 30, success codes `200`
- [ ] **Register targets:** none
- [ ] **After creation:** Attributes → deregistration delay **30** s

**5.2 Listener rule** (ALB → HTTP:80 listener → Add rule): 1 resource

- [ ] **Priority:** the service's priority
- [ ] **Condition:** **HTTP header** `X-Service-Name` = `devops2-g4-<svc>` (not a path condition)
- [ ] **Action:** forward to `devops2-g4-<svc>-tg-prod`

**5.3 ECS cluster** (ECS → Clusters → Create): 1 resource

- [ ] **Name:** `devops2-g4-<svc>-cluster-prod`
- [ ] **Infrastructure:** Fargate only
- [ ] **Monitoring:** Container Insights **on**

**5.4 Task definition** (ECS → Task definitions → Create): 1 resource

- [ ] **Family:** `devops2-g4-<svc>-prod`
- [ ] **Launch type / OS:** Fargate, Linux/X86_64
- [ ] **CPU / memory:** **1 vCPU, 2 GB**
- [ ] **Task role:** `devops2-g4-ecs-task-role-prod`
- [ ] **Task execution role:** `devops2-g4-ecs-task-execution-role-prod`
- [ ] **Container name:** the container name from the table, essential
- [ ] **Image:** `029637202701.dkr.ecr.ap-southeast-2.amazonaws.com/devops2-g4-<svc>-prod:15`
- [ ] **Port mapping:** the port, TCP
- [ ] **Environment variables:** `APP_ENV = prod`, `PORT = <port>`
- [ ] **Logging:** awslogs; group `/ecs/devops2-g4-app-prod`; region `ap-southeast-2`; stream prefix `ecs`. Untick "create log group".

**5.5 Service** (cluster → Services → Create): 1 resource

- [ ] **Launch type:** Fargate
- [ ] **Task definition:** the latest revision
- [ ] **Name:** `devops2-g4-<svc>-service-prod`
- [ ] **Desired tasks:** 2
- [ ] **Deployment:** min healthy **100%**, max **200%**
- [ ] **Networking:** the VPC, **both private subnets**, security group `ecs-sg` only, public IP **off**
- [ ] **Load balancing:** existing ALB, existing target group `devops2-g4-<svc>-tg-prod`, the container and port, health check grace period **60** s

**5.6 Auto scaling target** (service → Update → Service auto scaling): 1 resource

- [ ] **Tasks:** min **2**, max **10**

**5.7 Four step-scaling policies:** 4 resources

| ✓ | Name | Adjustment | Cooldown |
|---|---|---|---|
| ☐ | `devops2-g4-<svc>-cpu-scale-up-prod` | +1 when metric ≥ alarm threshold (lower bound 0) | 60 |
| ☐ | `devops2-g4-<svc>-cpu-scale-down-prod` | −1 (upper bound 0) | 300 |
| ☐ | `devops2-g4-<svc>-memory-scale-up-prod` | +1 (lower bound 0) | 60 |
| ☐ | `devops2-g4-<svc>-memory-scale-down-prod` | −1 (upper bound 0) | 300 |

All four use change-in-capacity and Average aggregation.

**5.8 Four CloudWatch alarms:** 4 resources

| ✓ | Alarm name | Metric (AWS/ECS) | Condition | Action |
|---|---|---|---|---|
| ☐ | `devops2-g4-<svc>-cpu-high-prod` | CPUUtilization | Average > 70 | cpu-scale-up |
| ☐ | `devops2-g4-<svc>-cpu-low-prod` | CPUUtilization | Average < 30 | cpu-scale-down |
| ☐ | `devops2-g4-<svc>-memory-high-prod` | MemoryUtilization | Average > 70 | memory-scale-up |
| ☐ | `devops2-g4-<svc>-memory-low-prod` | MemoryUtilization | Average < 30 | memory-scale-down |

All four alarms:
- **Dimensions:** ClusterName = `devops2-g4-<svc>-cluster-prod`, ServiceName = `devops2-g4-<svc>-service-prod`
- **Evaluation:** period 60 s, 2 evaluation periods
- **Descriptions:**
  - cpu-high: "Trigger scale up when CPU > 70%"
  - cpu-low: "Trigger scale down when CPU < 30%"
  - memory-high: "Trigger scale up when Memory > 70%"
  - memory-low: "Trigger scale down when Memory < 30%"

**5.9 API Gateway: two integrations and two routes** (API `devops2-g4-main-prod` → Routes): 4 resources

- [ ] **Route `ANY /<svc>/{proxy+}`:**
  - Integration: Private resource → ALB/NLB → `devops2-g4-shared-alb-prod`, listener HTTP 80, VPC link `devops2-g4-vpclink-prod`
  - Parameter mapping: **overwrite** `path` = `/$request.path.proxy`; **append** `header.X-Service-Name` = `devops2-g4-<svc>`
- [ ] **Route `ANY /<svc>`:**
  - A second integration, same as above
  - Parameter mapping: overwrite `path` = `/`; append `header.X-Service-Name` = `devops2-g4-<svc>`

When all 5 services are done, tick:
☐ auth ☐ profile ☐ messenger ☐ finance ☐ share

---

## 6. Count check

Expected total: 7 (state) + 17 (network) + 10 (security groups) + 5 (IAM) + 11 (logs, alerts, ALB, API) + 90 (services) = **140**, the same as one Terraform rebuild.

The CORS row in section 4 is a setting on the API, not a separate resource.

---

## 7. Finish

- [ ] **7.1** In ECS, each of the 5 services shows 2/2 tasks running.
- [ ] **7.2** Copy the API endpoint from API Gateway → `devops2-g4-main-prod` → Invoke URL.
- [ ] **7.3** Open `<endpoint>/auth`, `/profile`, `/messenger`, `/finance`, `/share`. When all 5 return a page (HTTP 200), **stop the timer**.
- [ ] **7.4** Run `./export.sh manual-run-N` (see README) before you delete anything.
