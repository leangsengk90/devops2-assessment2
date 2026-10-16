#!/usr/bin/env python3
"""Export the configuration of the devops2-g4 prod environment so two builds can be compared.

Usage:  python3 export.py <label>          e.g.  python3 export.py terraform-baseline
                                                  python3 export.py manual-run-1
Writes exports/<label>.json. Needs the AWS CLI configured for the account (read-only calls only).

Every resource is stored under a stable key built from its name (not its AWS id), and every AWS id
or ARN inside its settings is replaced by the name of the resource it points to, so a manual build and
a Terraform build of the same design produce comparable files. Live/volatile fields (timestamps,
states, IP addresses, DNS names, task counts) are dropped.
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REGION = "ap-southeast-2"
ENV = "prod"
SERVICES = ["auth", "messenger", "profile", "finance", "share"]
OUT = Path(__file__).resolve().parent / "exports"

VOLATILE = re.compile(
    r"(Time|Date|At|Timestamp)$|^(createdAt|updatedAt|registeredAt|registeredBy|deregisteredAt|events|deployments|"
    r"runningCount|pendingCount|desiredCount_live|status|State|state|Status|DNSName|CanonicalHostedZoneId|"
    r"NetworkInterfaceId|NetworkInterfaceIds|PrivateIpAddress|PublicIp|PublicIpv4Pool|AssociationId|AllocationId|"
    r"OwnerId|RoleId|RoleLastUsed|revision|ApiEndpoint|DeploymentId|LastModifiedDate|NatGatewayAddresses|"
    r"LoadBalancerAddresses|ItemCount|TableSizeBytes|TableId|TableArn|ProvisionedThroughput|WarmThroughput|"
    r"NumberOfDecreasesToday|statistics|activeServicesCount|pendingTasksCount|runningTasksCount|"
    r"registeredContainerInstancesCount|attachments|attachmentsStatus|capacityProviders|"
    r"defaultCapacityProviderStrategy|StateReason|StateReasonData|StateUpdatedTimestamp|StateValue|"
    r"AlarmConfigurationUpdatedTimestamp|EvaluationState|StateTransitionedTimestamp|IpOwner|"
    r"SecurityGroupRuleId|GroupId|VpcEndpointId|ResponseMetadata|MapPublicIpOnLaunch_live|AvailableIpAddressCount|"
    r"Ipv6CidrBlockAssociationSet|CidrBlockAssociationSet|DhcpOptionsId|InstanceTenancy|IsDefault|"
    r"PolicyARN|Alarms|SubnetArn|EnableLniAtDeviceIndex|createdBy|storedBytes|metricFilterCount)$")

ids = {}     # AWS id / ARN -> stable name


def aws(*args):
    cmd = ["aws", *args, "--region", REGION, "--output", "json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        if any(s in r.stderr for s in ("NotFound", "NoSuch", "does not exist", "cannot be found", "ResourceNotFound")):
            return None
        sys.stderr.write(f"warning: {' '.join(args[:2])}: {r.stderr.strip()[:200]}\n")
        return None
    return json.loads(r.stdout) if r.stdout.strip() else {}


def tagname(tags, default=None):
    for t in tags or []:
        if t.get("Key") == "Name":
            return t["Value"]
    return default


def remember(raw_id, name):
    if raw_id:
        ids[raw_id] = name


def clean(o):
    """Drop volatile keys, sort lists, keep everything else."""
    if isinstance(o, dict):
        return {k: clean(v) for k, v in sorted(o.items()) if not VOLATILE.search(k)}
    if isinstance(o, list):
        items = [clean(v) for v in o]
        return sorted(items, key=lambda x: json.dumps(x, sort_keys=True))
    return o


def resolve(o):
    """Replace AWS ids/ARNs by stable names (longest first so ARNs win over ids)."""
    s = json.dumps(o, sort_keys=True)
    for raw in sorted(ids, key=len, reverse=True):
        s = s.replace(raw, f"<{ids[raw]}>")
    return json.loads(s)


R = {}   # stable key -> settings


def put(key, settings):
    R[key] = settings


# ------------------------------------------------------------------ network
vpcs = (aws("ec2", "describe-vpcs", "--filters", f"Name=tag:Name,Values=devops2-g4-app-vpc-{ENV}") or {}).get("Vpcs", [])
vpc_id = vpcs[0]["VpcId"] if vpcs else None
for v in vpcs:
    remember(v["VpcId"], "vpc")
    attrs = {a: (aws("ec2", "describe-vpc-attribute", "--vpc-id", v["VpcId"], "--attribute", a) or {}).get(a[0].upper() + a[1:], {}).get("Value")
             for a in ("enableDnsHostnames", "enableDnsSupport")}
    put("vpc:" + tagname(v["Tags"]), {**v, **attrs})

if vpc_id:
    f = ["--filters", f"Name=vpc-id,Values={vpc_id}"]
    subnets = aws("ec2", "describe-subnets", *f)["Subnets"]
    for s in subnets:
        remember(s["SubnetId"], tagname(s.get("Tags"), s["SubnetId"]))
    for s in subnets:
        put("subnet:" + tagname(s.get("Tags"), s["SubnetId"]), s)
    for g in aws("ec2", "describe-internet-gateways", "--filters", f"Name=attachment.vpc-id,Values={vpc_id}")["InternetGateways"]:
        remember(g["InternetGatewayId"], tagname(g.get("Tags"), "igw"))
        put("igw:" + tagname(g.get("Tags"), "igw"), g)
    for e in aws("ec2", "describe-addresses", "--filters", "Name=tag:Name,Values=devops2-g4-app-nat-eip-*")["Addresses"]:
        remember(e["AllocationId"], tagname(e.get("Tags")))
        put("eip:" + tagname(e.get("Tags")), e)
    for n in aws("ec2", "describe-nat-gateways", "--filter", f"Name=vpc-id,Values={vpc_id}", "Name=state,Values=available,pending")["NatGateways"]:
        remember(n["NatGatewayId"], tagname(n.get("Tags"), n["NatGatewayId"]))
        put("nat:" + tagname(n.get("Tags"), n["NatGatewayId"]), n)
    for rt in aws("ec2", "describe-route-tables", *f)["RouteTables"]:
        main = any(a.get("Main") for a in rt.get("Associations", []))
        name = "main-route-table" if main else tagname(rt.get("Tags"), rt["RouteTableId"])
        remember(rt["RouteTableId"], name)
        if not main:
            put("route-table:" + name, rt)
    sgs = aws("ec2", "describe-security-groups", *f)["SecurityGroups"]
    for g in sgs:
        remember(g["GroupId"], g["GroupName"])
    for g in sgs:
        if g["GroupName"] == "default":
            continue
        g = {k: v for k, v in g.items() if k not in ("IpPermissions", "IpPermissionsEgress")}
        put("security-group:" + g["GroupName"], g)
        for rule in aws("ec2", "describe-security-group-rules", "--filters", f"Name=group-id,Values={g['GroupId']}")["SecurityGroupRules"]:
            direction = "egress" if rule["IsEgress"] else "ingress"
            target = rule.get("CidrIpv4") or ids.get((rule.get("ReferencedGroupInfo") or {}).get("GroupId"), "?")
            put(f"sg-rule:{g['GroupName']}:{direction}:{rule['IpProtocol']}:{rule.get('FromPort')}-{rule.get('ToPort')}:{target}",
                {k: v for k, v in rule.items() if k not in ("GroupOwnerId",)})

# ------------------------------------------------------------------ IAM
for role in (f"devops2-g4-ecs-task-execution-role-{ENV}", f"devops2-g4-ecs-task-role-{ENV}"):
    r = aws("iam", "get-role", "--role-name", role)
    if not r:
        continue
    r = r["Role"]
    remember(r["Arn"], role)
    put("iam-role:" + role, r)
    for p in (aws("iam", "list-attached-role-policies", "--role-name", role) or {}).get("AttachedPolicies", []):
        put(f"iam-attachment:{role}:{p['PolicyName']}", {"PolicyName": p["PolicyName"]})
    for pn in (aws("iam", "list-role-policies", "--role-name", role) or {}).get("PolicyNames", []):
        doc = aws("iam", "get-role-policy", "--role-name", role, "--policy-name", pn)
        put(f"iam-inline-policy:{role}:{pn}", {"PolicyDocument": doc.get("PolicyDocument")})

# ------------------------------------------------------------------ logs, SNS, EventBridge
for prefix in (f"/ecs/devops2-g4-app-{ENV}", f"/aws/apigateway/devops2-g4-main-{ENV}"):
    for lg in (aws("logs", "describe-log-groups", "--log-group-name-prefix", prefix) or {}).get("logGroups", []):
        if lg["logGroupName"] != prefix:
            continue
        remember(lg["arn"].rstrip(":*"), lg["logGroupName"])
        remember(lg["arn"], lg["logGroupName"])
        tags = (aws("logs", "list-tags-log-group", "--log-group-name", prefix) or {}).get("tags", {})
        put("log-group:" + prefix, {**lg, "Tags": tags})

topic = f"devops2-g4-app-inspector-findings-{ENV}"
for t in (aws("sns", "list-topics") or {}).get("Topics", []):
    if t["TopicArn"].endswith(":" + topic):
        remember(t["TopicArn"], topic)
        a = aws("sns", "get-topic-attributes", "--topic-arn", t["TopicArn"])["Attributes"]
        pol = json.loads(a.get("Policy", "{}"))
        put("sns-topic:" + topic, {"DisplayName": a.get("DisplayName"), "Tags": (aws("sns", "list-tags-for-resource", "--resource-arn", t["TopicArn"]) or {}).get("Tags")})
        put("sns-topic-policy:" + topic, {"Policy": pol})
rule = aws("events", "describe-rule", "--name", topic)
if rule:
    remember(rule["Arn"], topic)
    put("event-rule:" + topic, {**rule, "EventPattern": json.loads(rule.get("EventPattern", "{}"))})
    for t in (aws("events", "list-targets-by-rule", "--rule", topic) or {}).get("Targets", []):
        put(f"event-target:{topic}:{t['Id']}", t)

# ------------------------------------------------------------------ load balancer
lbs = (aws("elbv2", "describe-load-balancers", "--names", f"devops2-g4-shared-alb-{ENV}") or {}).get("LoadBalancers", [])
listeners = []
for lb in lbs:
    remember(lb["LoadBalancerArn"], lb["LoadBalancerName"])
    attrs = aws("elbv2", "describe-load-balancer-attributes", "--load-balancer-arn", lb["LoadBalancerArn"])["Attributes"]
    tags = aws("elbv2", "describe-tags", "--resource-arns", lb["LoadBalancerArn"])["TagDescriptions"][0]["Tags"]
    put("alb:" + lb["LoadBalancerName"], {**lb, "Attributes": attrs, "Tags": tags})
    listeners = aws("elbv2", "describe-listeners", "--load-balancer-arn", lb["LoadBalancerArn"])["Listeners"]
    for li in listeners:
        remember(li["ListenerArn"], f"listener-{li['Protocol']}-{li['Port']}")
tg_names = [f"devops2-g4-{s}-tg-{ENV}" for s in SERVICES]
tgs = (aws("elbv2", "describe-target-groups", "--names", *tg_names) or {}).get("TargetGroups", [])
if not tgs:   # describe fails if any name is missing; fall back to one by one
    for n in tg_names:
        tgs += (aws("elbv2", "describe-target-groups", "--names", n) or {}).get("TargetGroups", [])
for tg in tgs:
    remember(tg["TargetGroupArn"], tg["TargetGroupName"])
for tg in tgs:
    attrs = aws("elbv2", "describe-target-group-attributes", "--target-group-arn", tg["TargetGroupArn"])["Attributes"]
    tags = aws("elbv2", "describe-tags", "--resource-arns", tg["TargetGroupArn"])["TagDescriptions"][0]["Tags"]
    put("target-group:" + tg["TargetGroupName"], {**tg, "Attributes": attrs, "Tags": tags})
for li in listeners:
    put(f"listener:{li['Protocol']}-{li['Port']}", li)
    for rule in aws("elbv2", "describe-rules", "--listener-arn", li["ListenerArn"])["Rules"]:
        if rule["IsDefault"]:
            continue
        remember(rule["RuleArn"], f"listener-rule-{rule['Priority']}")
        put(f"listener-rule:{rule['Priority']}", rule)

# ------------------------------------------------------------------ API Gateway
for vl in (aws("apigatewayv2", "get-vpc-links") or {}).get("Items", []):
    if vl["Name"] == f"devops2-g4-vpclink-{ENV}":
        remember(vl["VpcLinkId"], vl["Name"])
        put("vpc-link:" + vl["Name"], vl)
for api in (aws("apigatewayv2", "get-apis") or {}).get("Items", []):
    if api["Name"] != f"devops2-g4-main-{ENV}":
        continue
    remember(api["ApiId"], api["Name"])
    put("http-api:" + api["Name"], api)
    for st in aws("apigatewayv2", "get-stages", "--api-id", api["ApiId"])["Items"]:
        put(f"api-stage:{st['StageName']}", st)
    integ = aws("apigatewayv2", "get-integrations", "--api-id", api["ApiId"])["Items"]
    routes = aws("apigatewayv2", "get-routes", "--api-id", api["ApiId"])["Items"]
    for rt in routes:
        iid = (rt.get("Target") or "").replace("integrations/", "")
        remember(iid, "integration-for " + rt["RouteKey"])
    for rt in routes:
        put("api-route:" + rt["RouteKey"], {k: v for k, v in rt.items() if k != "RouteId"})
    for it in integ:
        put("api-integration:" + ids.get(it["IntegrationId"], it["IntegrationId"]), {k: v for k, v in it.items() if k != "IntegrationId"})

# ------------------------------------------------------------------ ECS and scaling
for s in SERVICES:
    cname, sname = f"devops2-g4-{s}-cluster-{ENV}", f"devops2-g4-{s}-service-{ENV}"
    c = (aws("ecs", "describe-clusters", "--clusters", cname, "--include", "SETTINGS", "TAGS") or {}).get("clusters", [])
    c = [x for x in c if x.get("status") == "ACTIVE"]
    if not c:
        continue
    remember(c[0]["clusterArn"], cname)
    put("ecs-cluster:" + cname, c[0])
    sv = (aws("ecs", "describe-services", "--cluster", cname, "--services", sname, "--include", "TAGS") or {}).get("services", [])
    sv = [x for x in sv if x.get("status") == "ACTIVE"]
    if not sv:
        continue
    sv = sv[0]
    remember(sv["serviceArn"], sname)
    td = aws("ecs", "describe-task-definition", "--task-definition", sv["taskDefinition"], "--include", "TAGS")
    family = td["taskDefinition"]["family"]
    remember(sv["taskDefinition"], "taskdef-" + family)
    put("ecs-task-definition:" + family, {**td["taskDefinition"], "Tags": td.get("tags"), "taskDefinitionArn": None,
                                         "requiresAttributes": None, "compatibilities": None})
    put("ecs-service:" + sname, sv)
    rid = f"service/{cname}/{sname}"
    for t in (aws("application-autoscaling", "describe-scalable-targets", "--service-namespace", "ecs", "--resource-ids", rid) or {}).get("ScalableTargets", []):
        put("scaling-target:" + s, {k: v for k, v in t.items() if k not in ("ScalableTargetARN", "RoleARN")})
    for pol in (aws("application-autoscaling", "describe-scaling-policies", "--service-namespace", "ecs", "--resource-id", rid) or {}).get("ScalingPolicies", []):
        remember(pol["PolicyARN"], pol["PolicyName"])
        put("scaling-policy:" + pol["PolicyName"], pol)
for a in (aws("cloudwatch", "describe-alarms", "--alarm-name-prefix", "devops2-g4-") or {}).get("MetricAlarms", []):
    put("alarm:" + a["AlarmName"], {k: v for k, v in a.items() if k not in ("AlarmArn",)})

# ------------------------------------------------------------------ remote state
bucket = "devops2-g4-remote-state-029637202701"
b = {}
for name, args in [("Versioning", ["get-bucket-versioning"]), ("Encryption", ["get-bucket-encryption"]),
                   ("PublicAccessBlock", ["get-public-access-block"]), ("Cors", ["get-bucket-cors"]),
                   ("Lifecycle", ["get-bucket-lifecycle-configuration"]), ("Tags", ["get-bucket-tagging"])]:
    b[name] = aws("s3api", *args, "--bucket", bucket)
if any(b.values()):
    put("s3-bucket:" + bucket, b)
t = aws("dynamodb", "describe-table", "--table-name", "remote-state-locking")
if t:
    tt = t["Table"]
    put("dynamodb-table:remote-state-locking", {
        **tt, "TTL": (aws("dynamodb", "describe-time-to-live", "--table-name", "remote-state-locking") or {}).get("TimeToLiveDescription"),
        "Tags": (aws("dynamodb", "list-tags-of-resource", "--resource-arn", tt["TableArn"]) or {}).get("Tags")})

# ------------------------------------------------------------------ write
if len(sys.argv) != 2:
    sys.exit("usage: python3 export.py <label>")
OUT.mkdir(exist_ok=True)
data = {"label": sys.argv[1], "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "region": REGION, "resources": clean(resolve(R))}
path = OUT / f"{sys.argv[1]}.json"
path.write_text(json.dumps(data, indent=1, sort_keys=True))
print(f"exported {len(R)} resources to {path}")
