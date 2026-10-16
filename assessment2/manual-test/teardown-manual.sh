#!/usr/bin/env bash
# Delete everything a MANUAL run created (found by the names in CHECKLIST.md), so the next run starts empty.
# ECR repositories and images are never touched.
#
#   ./teardown-manual.sh                  dry run: prints what it would delete
#   CONFIRM=delete ./teardown-manual.sh   deletes
#
# Run it only after exporting the build (python3 export.py manual-run-N).
set -uo pipefail
export AWS_REGION=ap-southeast-2 AWS_DEFAULT_REGION=ap-southeast-2
ENV=prod
SERVICES="auth messenger profile finance share"
DRY=1; [ "${CONFIRM:-}" = delete ] && DRY=0

run() { if [ $DRY = 1 ]; then echo "would run: $*"; else echo "+ $*"; "$@" >/dev/null || echo "  (failed or already gone)"; fi; }
q() { aws "$@" --output text 2>/dev/null | grep -v '^None$' || true; }

# Safety: a Terraform-built environment keeps its state files in the bucket; a manual build does not.
if aws s3api list-objects-v2 --bucket devops2-g4-remote-state-029637202701 --prefix "env:/" --max-items 1 \
     --query 'Contents[0].Key' --output text 2>/dev/null | grep -q 'terraform.tfstate'; then
  echo "STOP: Terraform state files found in the state bucket, so this looks like the Terraform environment," >&2
  echo "not a manual build. Use prepare.sh (or destroy.sh) for the Terraform environment." >&2
  exit 1
fi

# ---------------- API Gateway (deleting the API removes its routes, integrations and stage)
API=$(q apigatewayv2 get-apis --query "Items[?Name=='devops2-g4-main-$ENV'].ApiId")
for a in $API; do run aws apigatewayv2 delete-api --api-id "$a"; done
VL=$(q apigatewayv2 get-vpc-links --query "Items[?Name=='devops2-g4-vpclink-$ENV'].VpcLinkId")
for v in $VL; do run aws apigatewayv2 delete-vpc-link --vpc-link-id "$v"; done

# ---------------- services
for s in $SERVICES; do
  C=devops2-g4-$s-cluster-$ENV; S=devops2-g4-$s-service-$ENV
  run aws cloudwatch delete-alarms --alarm-names "devops2-g4-$s-cpu-high-$ENV" "devops2-g4-$s-cpu-low-$ENV" "devops2-g4-$s-memory-high-$ENV" "devops2-g4-$s-memory-low-$ENV"
  run aws application-autoscaling deregister-scalable-target --service-namespace ecs --scalable-dimension ecs:service:DesiredCount --resource-id "service/$C/$S"
  run aws ecs delete-service --cluster "$C" --service "$S" --force
done
if [ $DRY = 0 ]; then
  for s in $SERVICES; do aws ecs wait services-inactive --cluster "devops2-g4-$s-cluster-$ENV" --services "devops2-g4-$s-service-$ENV" 2>/dev/null; done
fi
for s in $SERVICES; do
  run aws ecs delete-cluster --cluster "devops2-g4-$s-cluster-$ENV"
  for td in $(q ecs list-task-definitions --family-prefix "devops2-g4-$s-$ENV" --query 'taskDefinitionArns[]'); do
    run aws ecs deregister-task-definition --task-definition "$td"
    run aws ecs delete-task-definitions --task-definitions "$td"
  done
done

# ---------------- load balancer, listener rules, target groups
LB=$(q elbv2 describe-load-balancers --names "devops2-g4-shared-alb-$ENV" --query 'LoadBalancers[0].LoadBalancerArn')
for l in $LB; do
  for li in $(q elbv2 describe-listeners --load-balancer-arn "$l" --query 'Listeners[].ListenerArn'); do
    for r in $(q elbv2 describe-rules --listener-arn "$li" --query 'Rules[?IsDefault==`false`].RuleArn'); do run aws elbv2 delete-rule --rule-arn "$r"; done
  done
  run aws elbv2 delete-load-balancer --load-balancer-arn "$l"
  [ $DRY = 0 ] && aws elbv2 wait load-balancers-deleted --load-balancer-arns "$l"
done
for s in $SERVICES; do
  TG=$(q elbv2 describe-target-groups --names "devops2-g4-$s-tg-$ENV" --query 'TargetGroups[0].TargetGroupArn')
  for t in $TG; do run aws elbv2 delete-target-group --target-group-arn "$t"; done
done

# ---------------- alerts and logs
T=devops2-g4-app-inspector-findings-$ENV
run aws events remove-targets --rule "$T" --ids SendToSNS
for id in $(q events list-targets-by-rule --rule "$T" --query 'Targets[].Id'); do run aws events remove-targets --rule "$T" --ids "$id"; done
run aws events delete-rule --name "$T"
for tp in $(q sns list-topics --query "Topics[?ends_with(TopicArn, ':$T')].TopicArn"); do run aws sns delete-topic --topic-arn "$tp"; done
run aws logs delete-log-group --log-group-name "/ecs/devops2-g4-app-$ENV"
run aws logs delete-log-group --log-group-name "/aws/apigateway/devops2-g4-main-$ENV"

# ---------------- IAM
for role in devops2-g4-ecs-task-execution-role-$ENV devops2-g4-ecs-task-role-$ENV; do
  for p in $(q iam list-role-policies --role-name "$role" --query 'PolicyNames[]'); do run aws iam delete-role-policy --role-name "$role" --policy-name "$p"; done
  for p in $(q iam list-attached-role-policies --role-name "$role" --query 'AttachedPolicies[].PolicyArn'); do run aws iam detach-role-policy --role-name "$role" --policy-arn "$p"; done
  run aws iam delete-role --role-name "$role"
done

# ---------------- network
VPC=$(q ec2 describe-vpcs --filters "Name=tag:Name,Values=devops2-g4-app-vpc-$ENV" --query 'Vpcs[0].VpcId')
if [ -n "$VPC" ]; then
  [ $DRY = 0 ] && sleep 60   # let the load balancer, VPC link and task network interfaces disappear
  for sg in $(q ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC" --query "SecurityGroups[?GroupName!='default'].GroupId"); do
    for r in $(q ec2 describe-security-group-rules --filters "Name=group-id,Values=$sg" --query 'SecurityGroupRules[?IsEgress==`false`].SecurityGroupRuleId'); do run aws ec2 revoke-security-group-ingress --group-id "$sg" --security-group-rule-ids "$r"; done
    for r in $(q ec2 describe-security-group-rules --filters "Name=group-id,Values=$sg" --query 'SecurityGroupRules[?IsEgress==`true`].SecurityGroupRuleId'); do run aws ec2 revoke-security-group-egress --group-id "$sg" --security-group-rule-ids "$r"; done
  done
  for sg in $(q ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC" --query "SecurityGroups[?GroupName!='default'].GroupId"); do run aws ec2 delete-security-group --group-id "$sg"; done
  NATS=$(q ec2 describe-nat-gateways --filter "Name=vpc-id,Values=$VPC" "Name=state,Values=available,pending" --query 'NatGateways[].NatGatewayId')
  for n in $NATS; do run aws ec2 delete-nat-gateway --nat-gateway-id "$n"; done
  [ $DRY = 0 ] && [ -n "$NATS" ] && aws ec2 wait nat-gateway-deleted --nat-gateway-ids $NATS
  for e in $(q ec2 describe-addresses --filters "Name=tag:Name,Values=devops2-g4-app-nat-eip-*" --query 'Addresses[].AllocationId'); do run aws ec2 release-address --allocation-id "$e"; done
  for rt in $(q ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC" --query 'RouteTables[?Associations[0].Main!=`true`].RouteTableId'); do
    for a in $(q ec2 describe-route-tables --route-table-ids "$rt" --query 'RouteTables[0].Associations[?Main!=`true`].RouteTableAssociationId'); do run aws ec2 disassociate-route-table --association-id "$a"; done
    run aws ec2 delete-route-table --route-table-id "$rt"
  done
  for g in $(q ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=$VPC" --query 'InternetGateways[].InternetGatewayId'); do
    run aws ec2 detach-internet-gateway --internet-gateway-id "$g" --vpc-id "$VPC"
    run aws ec2 delete-internet-gateway --internet-gateway-id "$g"
  done
  for sn in $(q ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC" --query 'Subnets[].SubnetId'); do run aws ec2 delete-subnet --subnet-id "$sn"; done
  run aws ec2 delete-vpc --vpc-id "$VPC"
fi

# ---------------- remote-state bucket and lock table
B=devops2-g4-remote-state-029637202701
if aws s3api head-bucket --bucket "$B" 2>/dev/null; then
  if [ $DRY = 1 ]; then echo "would empty (all versions) and delete s3://$B"; else
    python3 - "$B" <<'PY'
import json, subprocess, sys
b = sys.argv[1]
while True:
    out = subprocess.run(["aws", "s3api", "list-object-versions", "--bucket", b, "--max-items", "500", "--output", "json"], capture_output=True, text=True).stdout or "{}"
    d = json.loads(out)
    objs = [{"Key": o["Key"], "VersionId": o["VersionId"]} for o in d.get("Versions", []) + d.get("DeleteMarkers", [])]
    if not objs:
        break
    subprocess.run(["aws", "s3api", "delete-objects", "--bucket", b, "--delete", json.dumps({"Objects": objs, "Quiet": True})], check=True, capture_output=True)
PY
    run aws s3api delete-bucket --bucket "$B"
  fi
fi
run aws dynamodb delete-table --table-name remote-state-locking

[ $DRY = 1 ] && echo -e "\nDry run only. Re-run with CONFIRM=delete to delete." || echo -e "\nTeardown finished. Re-run without CONFIRM to check nothing is left (it should print almost nothing)."
