#!/usr/bin/env python3
import os
import aws_cdk as cdk
from _stacks.eks_pipeline import EksClusterStack

app = cdk.App()

try:
    env = cdk.Environment(
        account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
        region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
    )
except KeyError as e:
    # Todo: 削除すること
    # todo: The following is for debugging of debugger
    env = cdk.Environment(
        account='338456725408',
        region='ap-northeast-1',
    )

eks_cluster_stack_dev = EksClusterStack(
    app,
    "EksAppStack",
    sys_env='dev',
    env=env)  # cdk.Environmentにすること

eks_cluster_stack_gitops = EksClusterStack(
    app,
    "EksGitopsStack",
    sys_env='gitops',
    env=env)  # cdk.Environmentにすること

app.synth()
