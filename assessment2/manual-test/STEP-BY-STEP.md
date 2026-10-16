# Manual AWS console build: step by step

This guide walks you, click by click, through creating the whole environment by hand in the AWS console. Every name and value matches the Terraform code, so your manual build can be compared with the Terraform one.

Expect about **1.5–2 hours** per build. Keep `recording-sheet.csv` open beside you.

---

## Part A: Before you start (not timed)

1. **Sign in** to the AWS console with the project account (`0296-3720-2701`).
2. **Set the region:** at the top right, choose **Asia Pacific (Sydney) ap-southeast-2**. Check it again whenever you open a new service.
3. **Make sure the account is empty:** run `CONFIRM=destroy ./prepare.sh` before your first run, or `CONFIRM=delete ./teardown-manual.sh` between runs. ECR → Repositories should still show the `devops2-g4-...-prod` repositories; don't touch them.
4. **Open the search bar** (top of the console, or press `Alt+S` / `Option+S`). You'll use it to jump between services: type `VPC`, `ECS`, `API Gateway`, and so on.
5. **Get your timer ready** (a phone stopwatch is fine).

### Tags (used on almost everything)

Most create pages have a **Tags** section at the bottom, usually under "Add new tag" or "Additional settings". Unless a step says otherwise, add:

| Key | Value |
|---|---|
| `Environment` | `prod` |
| `Service` | the value given in the step |
| `Name` | the resource name (some pages fill this in for you) |

### Mistakes

If you have to fix or delete and recreate something, add 1 to **mistakes_redone** and write a few words in **what_went_wrong**.

> ⏱ **Start the timer now**, at your first click on a "Create" button. Write the start time in the sheet.

---

## Part B: Terraform state storage (7 resources)

### B1. S3 bucket

1. Search **S3** → **Create bucket**.
2. **Bucket type:** General purpose. **Bucket name:** `devops2-g4-remote-state-029637202701`.
   - If AWS says the name is in use, wait one minute and try again; a just-deleted bucket name takes a moment to free up.
3. **Object Ownership:** ACLs disabled (default).
4. **Block Public Access settings:** keep **Block all public access** ticked.
5. **Bucket Versioning:** select **Enable**.
6. **Tags:**
   - `Name` = `devops2-g4-remote-state-029637202701`
   - `Environment` = `prod`
   - `Service` = `devops2-g4-remote-state-029637202701`
7. **Default encryption:** **Server-side encryption with Amazon S3 managed keys (SSE-S3)**. **Bucket Key:** select **Disable**.
8. Click **Create bucket**.
9. Open the bucket → **Permissions** tab → **Cross-origin resource sharing (CORS)** → **Edit** → paste the following, then **Save changes**:

   ```json
   [{"AllowedHeaders":["*"],"AllowedMethods":["GET","POST","PUT","DELETE"],"AllowedOrigins":["*"],"MaxAgeSeconds":3000}]
   ```

10. **Management** tab → **Create lifecycle rule**:
    - Name `cleanup-old-versions`; scope **Apply to all objects** (tick the acknowledgement)
    - Rule actions: tick **Permanently delete noncurrent versions of objects**; days after objects become noncurrent: `30`
    - **Create rule**
11. **Create lifecycle rule** again:
    - Name `expire-temp-files`; scope **Limit the scope using filters**; prefix `temp/`
    - Rule actions: tick **Expire current versions of objects**; days: `7`
    - **Create rule**

### B2. DynamoDB table

1. Search **DynamoDB** → **Tables** → **Create table**.
2. **Table name** `remote-state-locking`; **Partition key** `LockID`, type **String**. No sort key.
3. **Table settings:** **Customize settings**:
   - **Table class:** DynamoDB Standard
   - **Read/write capacity:** **On-demand**
   - **Encryption:** **Owned by Amazon DynamoDB**
4. **Tags:**
   - `Environment` = `prod`
   - `Service` = `remote-state-locking`
5. **Create table**. Wait until its status is **Active**.
6. Open the table → **Additional settings** tab → **Time to Live (TTL)** → **Turn on**. TTL attribute name `TimeToExist` → **Turn on TTL**.

---

## Part C: Network (17 resources)

Search **VPC** to open the VPC console. Use **Your VPCs**, **Subnets** and the other pages in the left menu. **Do not use "VPC and more"**: choose **VPC only**, so every piece matches Terraform.

For every resource in Part C, use tags `Environment` = `prod` and `Service` = `devops2-g4-app`.

### C1. VPC

1. **Your VPCs** → **Create VPC** → **VPC only**.
2. **Name tag** `devops2-g4-app-vpc-prod`; **IPv4 CIDR** `10.0.0.0/16`; no IPv6; tenancy Default.
3. Add tags → **Create VPC**.
4. On the VPC: **Actions → Edit VPC settings** → tick **Enable DNS resolution** and **Enable DNS hostnames** → **Save**.

### C2. Four subnets

1. **Subnets** → **Create subnet** → choose VPC `devops2-g4-app-vpc-prod`.
2. Add these four on one page with **Add new subnet** (tags on each):

| Subnet name | Availability Zone | IPv4 subnet CIDR |
|---|---|---|
| `devops2-g4-app-public-subnet-ap-southeast-2a-prod` | ap-southeast-2a | `10.0.1.0/24` |
| `devops2-g4-app-public-subnet-ap-southeast-2b-prod` | ap-southeast-2b | `10.0.2.0/24` |
| `devops2-g4-app-private-subnet-ap-southeast-2a-prod` | ap-southeast-2a | `10.0.11.0/24` |
| `devops2-g4-app-private-subnet-ap-southeast-2b-prod` | ap-southeast-2b | `10.0.12.0/24` |

3. **Create subnet**.
4. For **each of the two public subnets:** select it → **Actions → Edit subnet settings** → tick **Enable auto-assign public IPv4 address** → **Save**.

### C3. Internet gateway

1. **Internet gateways** → **Create internet gateway** → Name `devops2-g4-app-igw-prod` (+ tags) → **Create**.
2. **Actions → Attach to VPC** → `devops2-g4-app-vpc-prod` → **Attach**.

### C4. Two Elastic IPs

**Elastic IPs** → **Allocate Elastic IP address** → Amazon's pool → tags with `Name` = `devops2-g4-app-nat-eip-ap-southeast-2a-prod` → **Allocate**. Repeat with `Name` = `devops2-g4-app-nat-eip-ap-southeast-2b-prod`.

### C5. Two NAT gateways

1. **NAT gateways** → **Create NAT gateway**:
   - Name `devops2-g4-app-nat-gateway-ap-southeast-2a-prod`
   - **Subnet:** the **public** subnet **2a**
   - Connectivity **Public**
   - **Elastic IP:** the **2a** EIP
   - Tags → **Create**
2. Repeat for **2b**: name `...-nat-gateway-ap-southeast-2b-prod`, the public subnet 2b, and the 2b EIP.
3. They take 1–2 minutes to become **Available**. Carry on meanwhile.

### C6. Route tables (3 tables, 4 associations)

1. **Route tables** → **Create route table** → Name `devops2-g4-app-public-rt-prod`, VPC `devops2-g4-app-vpc-prod`, tags → **Create**.
   - **Routes** tab → **Edit routes** → **Add route**: destination `0.0.0.0/0`, target **Internet Gateway** → `devops2-g4-app-igw-prod` → **Save**.
   - **Subnet associations** tab → **Edit subnet associations** → tick **both public subnets** → **Save**.
2. **Create route table** → Name `devops2-g4-app-private-rt-ap-southeast-2a-prod` → **Create**.
   - Routes: `0.0.0.0/0` → **NAT Gateway** → the **2a** NAT gateway.
   - Associations: **private subnet 2a** only.
3. **Create route table** → Name `devops2-g4-app-private-rt-ap-southeast-2b-prod`.
   - Routes: `0.0.0.0/0` → the **2b** NAT gateway.
   - Associations: **private subnet 2b** only.

---

## Part D: Security groups (3 groups + 7 rules)

Go to **VPC → Security groups** (or **EC2 → Security groups**).

Because the groups point at each other, **create all three empty first, then add the rules.** Every group gets tags `Environment` = `prod` and `Service` = `devops2-g4-app`.

### D1. Create three empty groups

For each row: **Create security group** → name and description → VPC `devops2-g4-app-vpc-prod` → **remove** the default outbound rule (click **Delete** next to it) → tags → **Create**.

| Security group name | Description |
|---|---|
| `devops2-g4-alb-sg-prod` | `Security group for Application Load Balancer` |
| `devops2-g4-ecs-sg-prod` | `Security group for ECS Fargate tasks` |
| `devops2-g4-vpclink-sg-prod` | `Security group for API Gateway VPC Link` |

### D2. Add the rules

Select a group → **Inbound rules** (or **Outbound rules**) tab → **Edit** → **Add rule** → **Save rules**.

| Group | Tab | Type | Port range | Source / Destination | Description |
|---|---|---|---|---|---|
| alb-sg | Inbound | HTTP | 80 | Custom `10.0.0.0/16` | `Allow HTTP from VPC Link` |
| alb-sg | Inbound | HTTPS | 443 | Custom `10.0.0.0/16` | `Allow HTTPS from VPC Link` |
| alb-sg | Outbound | Custom TCP | `0-65535` | `devops2-g4-ecs-sg-prod` | `Allow all outbound to ECS tasks` |
| ecs-sg | Inbound | Custom TCP | `0-65535` | `devops2-g4-alb-sg-prod` | `Allow traffic from ALB` |
| ecs-sg | Outbound | All traffic | All | `0.0.0.0/0` | `Allow all outbound traffic` |
| vpclink-sg | Inbound | HTTPS | 443 | Anywhere-IPv4 `0.0.0.0/0` | `Allow HTTPS from anywhere` |
| vpclink-sg | Outbound | Custom TCP | `0-65535` | `devops2-g4-alb-sg-prod` | `Allow traffic to ALB` |

To pick a security group as source or destination, choose **Custom** and start typing `sg-` or the group name.

---

## Part E: IAM roles (2 roles)

Search **IAM** → **Roles** → **Create role**.

### E1. Execution role

1. **Trusted entity type:** AWS service. **Use case:** **Elastic Container Service** → **Elastic Container Service Task** → **Next**.
2. **Add permissions:** search and tick `AmazonECSTaskExecutionRolePolicy` → **Next**.
3. **Role name** `devops2-g4-ecs-task-execution-role-prod`; tags `Environment` = `prod`, `Service` = `devops2-g4-app` → **Create role**.
4. Open the role → **Add permissions → Create inline policy** → **JSON** tab → paste:

   ```json
   {"Version":"2012-10-17","Statement":[
    {"Effect":"Allow","Action":["ecr:GetAuthorizationToken","ecr:BatchCheckLayerAvailability","ecr:GetDownloadUrlForLayer","ecr:BatchGetImage"],"Resource":"*"},
    {"Effect":"Allow","Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],"Resource":"arn:aws:logs:ap-southeast-2:*:log-group:/ecs/*"}]}
   ```

5. **Next** → policy name `devops2-g4-ecs-task-execution-role-inline-policy-prod` → **Create policy**.

### E2. Task role

1. **Create role** → same trusted entity (**Elastic Container Service Task**) → **Next**.
2. **Do not add any managed policy** → **Next**.
3. Name `devops2-g4-ecs-task-role-prod`, same tags → **Create role**.
4. **Add permissions → Create inline policy → JSON**:

   ```json
   {"Version":"2012-10-17","Statement":[
    {"Effect":"Allow","Action":["s3:GetObject","s3:PutObject","s3:ListBucket"],"Resource":["arn:aws:s3:::devops2-g4-*","arn:aws:s3:::devops2-g4-*/*"]},
    {"Effect":"Allow","Action":["dynamodb:GetItem","dynamodb:PutItem","dynamodb:UpdateItem","dynamodb:Query","dynamodb:Scan"],"Resource":"arn:aws:dynamodb:ap-southeast-2:*:table/devops2-g4-*"},
    {"Effect":"Allow","Action":["ssm:GetParameter","ssm:GetParameters"],"Resource":"arn:aws:ssm:ap-southeast-2:*:parameter/devops2-g4/*"}]}
   ```

5. Policy name `devops2-g4-ecs-task-role-inline-policy-prod` → **Create policy**.

---

## Part F: Logs and alert topic

### F1. Two log groups

Search **CloudWatch** → **Logs → Log groups** → **Create log group**:

| Log group name | Retention | Service tag |
|---|---|---|
| `/ecs/devops2-g4-app-prod` | 1 week (7 days) | `devops2-g4-app` |
| `/aws/apigateway/devops2-g4-main-prod` | 1 week (7 days) | `devops2-g4-main` |

Both also get `Environment` = `prod` and `Name` = the log group name.

### F2. SNS topic

1. Search **SNS** → **Topics** → **Create topic** → **Standard**.
2. Name `devops2-g4-app-inspector-findings-prod`.
3. **Access policy:** **Advanced** → replace the JSON with the following, putting the topic ARN in place of `TOPIC_ARN`. The default policy shows it at `"Resource"`; copy it from there first.

   ```json
   {"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"events.amazonaws.com"},"Action":"sns:Publish","Resource":"TOPIC_ARN"}]}
   ```

4. Tags `Environment` = `prod`, `Service` = `devops2-g4-app`, `ManagedBy` = `terraform` → **Create topic**.

### F3. EventBridge rule

1. Search **EventBridge** → **Rules** → **Create rule**.
2. Name `devops2-g4-app-inspector-findings-prod`, description `Capture Inspector findings`, event bus **default**, **Rule with an event pattern** → **Next**.
3. **Event source:** AWS events. **Creation method:** **Custom pattern (JSON editor)** → paste:

   ```json
   {"source":["aws.inspector2"],"detail-type":["Inspector2 Finding"]}
   ```

4. **Next** → **Target:** AWS service → **SNS topic** → `devops2-g4-app-inspector-findings-prod` → **Next**.
5. Tags `Environment` = `prod`, `Service` = `devops2-g4-app`, `ManagedBy` = `terraform` → **Create rule**.

---

## Part G: Load balancer and API Gateway

### G1. Application Load Balancer

1. Search **EC2** → **Load Balancers** → **Create load balancer** → **Application Load Balancer** → **Create**.
2. **Basic configuration:**
   - Name `devops2-g4-shared-alb-prod`
   - Scheme **Internal**
   - IP address type **IPv4**
3. **Network mapping:** VPC `devops2-g4-app-vpc-prod`; tick **ap-southeast-2a** → **private** subnet 2a, and **ap-southeast-2b** → **private** subnet 2b.
4. **Security groups:** remove `default`; choose `devops2-g4-alb-sg-prod` only.
5. **Listeners and routing:** HTTP : 80. **Default action:** **Return fixed response**, response code `404`, content type `text/plain`, body `Service not found`.
   - If this console version only offers "Forward to", create it with a temporary action, then change the listener's default action to the fixed response straight after.
6. Tags:
   - `Name` = `devops2-g4-shared-alb-prod`
   - `Environment` = `prod`
   - `Service` = `devops2-g4-shared`
7. **Create load balancer.** It takes a few minutes to become **Active**; carry on.

### G2. VPC link

1. Search **API Gateway** → left menu **VPC links** → **Create** → **VPC link for HTTP APIs**.
2. Name `devops2-g4-vpclink-prod`; VPC `devops2-g4-app-vpc-prod`; subnets: **both private subnets**; security group `devops2-g4-vpclink-sg-prod` only.
3. Tags:
   - `Name` = `devops2-g4-vpclink-prod`
   - `Environment` = `prod`
   - `Service` = `devops2-g4-main`
4. **Create.** It takes a few minutes to become **Available**.

### G3. HTTP API

1. **API Gateway** → **APIs** → **Create API** → **HTTP API** → **Build**.
2. API name `devops2-g4-main-prod`; **don't add integrations yet** → **Next**.
3. **Routes:** add none → **Next**.
4. **Stages:** keep `$default` with **Auto-deploy** on → **Next** → **Create**.
5. Open the API:
   - **Description** (API details → Edit): `Main API Gateway for all microservices`.
   - **CORS** (left menu) → **Configure**:
     - Access-Control-Allow-Origin `*`
     - Allow-Methods GET, POST, PUT, DELETE, OPTIONS
     - Allow-Headers `*`
     - Max-Age `300`
     - **Save**
   - **Stages → $default → Edit**: throttling burst `5000`, rate `10000` → **Save**.
   - **Monitor → Logging → Edit** (on the $default stage):
     - Turn on access logging. Destination: the ARN of log group `/aws/apigateway/devops2-g4-main-prod` (copy it from CloudWatch).
     - Log format:

       ```json
       {"requestId":"$context.requestId","ip":"$context.identity.sourceIp","requestTime":"$context.requestTime","httpMethod":"$context.httpMethod","routeKey":"$context.routeKey","status":"$context.status","protocol":"$context.protocol","responseLength":"$context.responseLength"}
       ```

   - **Tags:**
     - `Name` = `devops2-g4-main-prod`
     - `Environment` = `prod`
     - `Service` = `devops2-g4-main`

---

## Part H: The five services (do H1–H9 five times)

Do **auth** first, then profile, messenger, finance and share. Wherever you see `<svc>`, type the service name.

| `<svc>` | Container name | Port | Health check path | Priority | Route |
|---|---|---|---|---|---|
| auth | `auth-app` | `3000` | `/` | `200` | `/auth` |
| profile | `profile-app` | `3001` | `/` | `300` | `/profile` |
| messenger | `messenger-app` | `3002` | `/` | `400` | `/messenger` |
| finance | `finance-app` | `8080` | `/api/hello` | `500` | `/finance` |
| share | `share-app` | `3004` | `/` | `600` | `/share` |

Tags for everything in Part H: `Environment` = `prod`, `Service` = `devops2-g4-<svc>`.

### H1. Target group

1. **EC2** → **Target groups** → **Create target group**.
2. **Target type:** **IP addresses**. **Name** `devops2-g4-<svc>-tg-prod`. **Protocol** HTTP, **port** = the service's port. VPC `devops2-g4-app-vpc-prod`. Protocol version HTTP1.
3. **Health checks:** HTTP, path = the service's path. **Advanced health check settings:**
   - Healthy threshold `2`
   - Unhealthy threshold `3`
   - Timeout `5`
   - Interval `30`
   - Success codes `200`
4. Tags → **Next** → don't register any targets → **Create target group**.
5. Open it → **Attributes** tab → **Edit** → **Deregistration delay** `30` seconds → **Save**.

### H2. Listener rule

1. **Load Balancers** → `devops2-g4-shared-alb-prod` → **Listeners and rules** → **HTTP:80** → **Add rule**.
2. Name tag (optional) → **Next**.
3. **Add condition** → **HTTP header**. Header name `X-Service-Name`, value `devops2-g4-<svc>`.
   - ⚠ Use HTTP **header**, not Path. This is the most common mistake.
4. **Next** → **Action:** **Forward to target groups** → `devops2-g4-<svc>-tg-prod` → **Next**.
5. **Priority** = the service's priority → **Next** → **Create**.

### H3. ECS cluster

1. Search **ECS** → **Clusters** → **Create cluster**.
2. Name `devops2-g4-<svc>-cluster-prod`. **Infrastructure:** **AWS Fargate (serverless)** only.
3. **Monitoring:** turn on **Container Insights** (choose standard Container Insights, not enhanced).
4. Tags → **Create**.

### H4. Task definition

1. **ECS** → **Task definitions** → **Create new task definition**.
2. **Family** `devops2-g4-<svc>-prod`.
3. **Infrastructure:**
   - Launch type **AWS Fargate**
   - OS **Linux/X86_64**
   - CPU **1 vCPU**, memory **2 GB**
   - **Task role** `devops2-g4-ecs-task-role-prod`
   - **Task execution role** `devops2-g4-ecs-task-execution-role-prod`
4. **Container – 1:**
   - Name = the container name; **Image URI** `029637202701.dkr.ecr.ap-southeast-2.amazonaws.com/devops2-g4-<svc>-prod:15`; **Essential** Yes.
   - **Port mappings:** container port = the service's port, TCP. Delete any extra port mapping or port name the console adds.
   - **Environment variables:** add `APP_ENV` = `prod` and `PORT` = the service's port.
   - **Log collection:** on, **Amazon CloudWatch**:
     - `awslogs-group` = `/ecs/devops2-g4-app-prod`
     - `awslogs-region` = `ap-southeast-2`
     - `awslogs-stream-prefix` = `ecs`
     - Remove `awslogs-create-group` if it's there.
   - Leave container health check empty.
5. Tags → **Create**.

### H5. ECS service

1. **Clusters** → `devops2-g4-<svc>-cluster-prod` → **Services** tab → **Create**.
2. **Compute options:** **Launch type** → **FARGATE**, platform **LATEST**.
3. **Deployment configuration:**
   - **Application type:** Service
   - **Family** `devops2-g4-<svc>-prod`, latest revision
   - **Service name** `devops2-g4-<svc>-service-prod`
   - **Desired tasks** `2`
   - Deployment options: **Min running tasks** `100` %, **Max running tasks** `200` %
   - Turn **off** the deployment circuit breaker if it's on by default, because Terraform doesn't use it.
4. **Networking:**
   - VPC `devops2-g4-app-vpc-prod`
   - Subnets: **only the two private subnets**
   - Security group: **existing** `devops2-g4-ecs-sg-prod` only (remove default)
   - **Public IP: off**
5. **Load balancing:**
   - Application Load Balancer → **Use an existing load balancer** → `devops2-g4-shared-alb-prod`
   - Container: choose the container and port
   - **Use an existing listener** HTTP:80
   - **Use an existing target group** `devops2-g4-<svc>-tg-prod`
   - **Health check grace period** `60` seconds
6. **Service auto scaling:** leave off here; you'll add it in H6.
7. Tags → **Create**.

### H6. Auto scaling and four scaling policies

1. Open the service → **Update service**. Find **Service auto scaling** → **Use service auto scaling**:
   - Minimum tasks `2`, maximum tasks `10`.
   - Choose **Step scaling**.
2. Add the four policies below. If the ECS page only offers target tracking, set min/max here and add the step policies through CloudWatch alarms instead (step H7). Each policy name, adjustment and cooldown is in the table.

| Policy name | Adjustment | Step bound | Cooldown |
|---|---|---|---|
| `devops2-g4-<svc>-cpu-scale-up-prod` | Add 1 task | lower bound 0 | 60 s |
| `devops2-g4-<svc>-cpu-scale-down-prod` | Remove 1 task | upper bound 0 | 300 s |
| `devops2-g4-<svc>-memory-scale-up-prod` | Add 1 task | lower bound 0 | 60 s |
| `devops2-g4-<svc>-memory-scale-down-prod` | Remove 1 task | upper bound 0 | 300 s |

All four use adjustment type **Change in capacity** and metric aggregation **Average**.

### H7. Four CloudWatch alarms

1. **CloudWatch** → **Alarms** → **Create alarm** → **Select metric** → **ECS** → **ClusterName, ServiceName** → tick the metric for this service.
2. **Statistic** Average, **period** 1 minute.
3. **Conditions:** static, threshold as in the table. **Additional configuration:** datapoints to alarm `2` out of `2`.
4. **Actions:** remove the default notification. **Add Auto Scaling action** → ECS service → this service → the matching policy.
5. Name and description as below → **Create alarm**.

| Alarm name | Metric | Condition | Action (policy) | Description |
|---|---|---|---|---|
| `devops2-g4-<svc>-cpu-high-prod` | CPUUtilization | Greater than `70` | cpu-scale-up | `Trigger scale up when CPU > 70%` |
| `devops2-g4-<svc>-cpu-low-prod` | CPUUtilization | Lower than `30` | cpu-scale-down | `Trigger scale down when CPU < 30%` |
| `devops2-g4-<svc>-memory-high-prod` | MemoryUtilization | Greater than `70` | memory-scale-up | `Trigger scale up when Memory > 70%` |
| `devops2-g4-<svc>-memory-low-prod` | MemoryUtilization | Lower than `30` | memory-scale-down | `Trigger scale down when Memory < 30%` |

Tags on each alarm: `Environment` = `prod`, `Service` = `devops2-g4-<svc>`.

### H8. Two API routes and integrations

**Route 1 (sub-paths):**

1. **API Gateway** → `devops2-g4-main-prod` → **Routes** → **Create**. Method **ANY**, path `/<svc>/{proxy+}` → **Create**.
2. Select the route → **Attach integration** → **Create and attach an integration**.
3. **Integration type:** **Private resource**. **Target service:** **ALB/NLB**. **Load balancer** `devops2-g4-shared-alb-prod`. **Listener** HTTP 80. **VPC link** `devops2-g4-vpclink-prod` → **Create**.
4. Left menu **Integrations** → select this integration → **Parameter mapping** → **Create parameter mapping** for **all incoming requests**:
   - **Overwrite** `path` → value `/$request.path.proxy`
   - **Append** `header.X-Service-Name` → value `devops2-g4-<svc>`
   - **Create**

**Route 2 (root path):**

1. **Create** route **ANY** `/<svc>` → **Create**.
2. **Attach integration** → **create a new one**, not the one from route 1, with the same private ALB settings.
3. Parameter mapping:
   - **Overwrite** `path` → `/`
   - **Append** `header.X-Service-Name` → `devops2-g4-<svc>`

### H9. Check this service before moving on

**ECS → cluster → service:** wait until **2/2 tasks running** and the target group shows **2 healthy** targets.

Then go back to H1 for the next service. When all five are done, tick them on your sheet:

☐ auth ☐ profile ☐ messenger ☐ finance ☐ share

---

## Part I: Finish and stop the timer

1. **API Gateway** → `devops2-g4-main-prod` → copy the **Invoke URL**, e.g. `https://abc123.execute-api.ap-southeast-2.amazonaws.com`.
2. Open these five URLs in your browser:
   - `<Invoke URL>/auth`
   - `<Invoke URL>/profile`
   - `<Invoke URL>/messenger`
   - `<Invoke URL>/finance`
   - `<Invoke URL>/share`
3. When **all five load (HTTP 200)**, ⏱ **stop the timer**. Write the end time in the sheet. Take a screenshot as evidence.
4. Fill the rest of the row:
   - `resources_created` (140 if you followed every step)
   - `mistakes_redone`
   - `services_running_of_5`
   - `http_200_of_5`
   - notes
5. In the terminal, from `assessment2/manual-test/`, export before you delete anything:

   ```
   python3 export.py manual-run-1
   python3 compare.py exports/terraform-baseline.json exports/manual-run-1.json
   ```

6. Delete the build so the next run starts empty:

   ```
   ./teardown-manual.sh                  # check the list first
   CONFIRM=delete ./teardown-manual.sh
   ```

---

## If something goes wrong

| Problem | Likely cause and fix |
|---|---|
| ECS tasks keep stopping with "CannotPullContainerError" | The task is in a subnet with no NAT route, or the execution role is wrong. Check the private route tables point to the NAT gateways (C6) and that the execution role is chosen (H4). |
| Tasks run but the target group shows **unhealthy** | Wrong port or health check path (H1), or ecs-sg doesn't allow traffic from alb-sg (D2). Finance must use `/api/hello`. |
| URL returns `Service not found` (404) | The listener rule condition is wrong. It must be **HTTP header** `X-Service-Name = devops2-g4-<svc>` (H2), and the integration must append that header (H8). |
| URL returns `503` / `Service Unavailable` | The VPC link isn't **Available** yet, or vpclink-sg can't reach alb-sg (D2). Wait, then check the rules. |
| URL returns `404 Not Found` from API Gateway | The route path is wrong. It needs both `/<svc>` and `/<svc>/{proxy+}` (H8). |
| S3 bucket name "already exists" | Wait a minute after a teardown and try again. |

Each fix counts as a mistake on your sheet. That's real data, so record it honestly.
