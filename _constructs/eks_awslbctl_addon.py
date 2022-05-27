import json
from constructs import Construct
from aws_cdk import aws_iam
from aws_cdk import aws_eks


class AwsLoadBalancerController(Construct):
    # ----------------------------------------------------------
    # AWS LoadBalancer Controllerをdeployする
    # IngressのannotationでALBを作成する
    # ----------------------------------------------------------

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        self.region = kwargs.get('region')
        self.cluster: aws_eks.Cluster = kwargs.get('cluster')

    def deploy(self):
        # ----------------------------------------------------------
        # AWS LoadBalancer Controller for AWS ALB
        #   - Service Account
        #   - Namespace: kube-system
        #   - Deployment
        #   - Service
        # ----------------------------------------------------------
        awslbcontroller_sa = self.cluster.add_service_account(
            'LBControllerServiceAccount',
            name='aws-load-balancer-controller',  # fixed name
            namespace='kube-system',
        )

        statements = []
        with open('./policies/awslbcontroller-policy.json') as f:
            data = json.load(f)
            for statement in data['Statement']:
                statements.append(aws_iam.PolicyStatement.from_json(statement))

        policy = aws_iam.Policy(
            self, 'AWSLoadBalancerControllerIAMPolicy', statements=statements)
        policy.attach_to_role(awslbcontroller_sa.role)

        aws_lb_controller_chart = self.cluster.add_helm_chart(
            'AwsLoadBalancerController',
            chart='aws-load-balancer-controller',
            release='aws-load-balancer-controller',  # Deployment name
            repository='https://aws.github.io/eks-charts',
            version=None,
            namespace='kube-system',
            create_namespace=False,
            values={
                'clusterName': self.cluster.cluster_name,
                'serviceAccount': {
                    'name': awslbcontroller_sa.service_account_name,
                    'create': False,
                    'annotations': {
                        'eks.amazonaws.com/role-arn': awslbcontroller_sa.role.role_arn
                    }
                }
            }
        )
        aws_lb_controller_chart.node.add_dependency(awslbcontroller_sa)
