import json
from constructs import Construct
from aws_cdk import aws_iam


class AwsLoadBalancerController(Construct):
    # ----------------------------------------------------------
    # AWS LoadBalancer Controllerをdeployする
    # IngressのannotationでALBを作成する
    # ----------------------------------------------------------

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        self.region = kwargs.get('region')
        self.cluster = kwargs.get('cluster')
        pass

    def deploy(self):
        # ----------------------------------------------------------
        # AWS LoadBalancer Controller for AWS ALB
        #   - Service Account
        #   - Namespace: kube-system
        #   - Deployment
        #   - Service
        # ----------------------------------------------------------
        # _cluster = self.resources.get('cluster')
        # awslbcontroller_sa = _cluster.add_service_account(
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

        # vpc = self.resources.get('vpc')

        # aws_lb_controller_chart = _cluster.add_helm_chart(
        aws_lb_controller_chart = self.cluster.add_helm_chart(
            'AwsLoadBalancerController',
            chart='aws-load-balancer-controller',
            release='aws-load-balancer-controller',  # Deploymentの名前になる。
            repository='https://aws.github.io/eks-charts',
            version=None,
            namespace='kube-system',
            create_namespace=False,
            values={
                # 'clusterName': _cluster.cluster_name,
                'clusterName': self.cluster.cluster_name,
                # 'region': self.region,
                # 'vpcId': vpc.vpc_id,
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
