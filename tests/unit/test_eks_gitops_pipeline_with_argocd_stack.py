import aws_cdk as core
import aws_cdk.assertions as assertions

from _stacks.eks_gitops_pipeline_with_argocd_stack import EksGitopsPipelineWithArgocdStack

# example tests. To run these tests, uncomment this file along with the example
# resource in eks_gitops_pipeline_with_argocd/eks_gitops_pipeline_with_argocd_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EksGitopsPipelineWithArgocdStack(app, "eks-gitops-pipeline-with-argocd")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
