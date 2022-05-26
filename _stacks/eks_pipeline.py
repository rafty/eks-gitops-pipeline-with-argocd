import json
import yaml
# import humps
import aws_cdk
from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import aws_iam
from aws_cdk import aws_eks
from util.configure.config import Config
from _constructs.eks import EksCluster


class EksClusterStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            sys_env: str,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.config = Config(self, 'UtilConfig', sys_env)
        _env = kwargs['env']
        self.config.env.region = _env.region
        self.config.env.account = _env.account

        self.resources = {
            # 'vpc': None,
            # 'cluster': None,
        }

        _eks_cluster = EksCluster(self, 'EksCluster', self.config)
        _eks_cluster.provisioning()

        # self.create_eks_cluster()

    # def create_eks_cluster(self):
    #     # --------------------------------------------------------------
    #     # EKS Cluster
    #     #   Owner role for EKS Cluster
    #     # --------------------------------------------------------------
    #
    #     i_vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_name=self.config.vpc.name)
    #     eks_cluster_name = ''.join([self.config.eks.name, '_', self.config.env.name])
    #     # app_eks_dev, gitops_eks_gitops
    #
    #     _owner_role = aws_iam.Role(
    #         scope=self,
    #         id='EksClusterOwnerRole',
    #         role_name=f'{self.config.env.name}EksClusterOwnerRole',
    #         # id=f'{cluster_name_pascal}EksClusterOwnerRole',
    #         # role_name=f'{cluster_name_pascal}EksClusterOwnerRole',
    #         assumed_by=aws_iam.AccountRootPrincipal()
    #     )
    #
    #     self.resources['cluster'] = aws_eks.Cluster(
    #         self,
    #         'EksCluster',
    #         cluster_name=self.config.eks.name,
    #         version=aws_eks.KubernetesVersion.V1_21,
    #         default_capacity_type=aws_eks.DefaultCapacityType.NODEGROUP,
    #         default_capacity=1,
    #         default_capacity_instance=aws_ec2.InstanceType(self.config.eks.instance_type),
    #         # default_capacity_instance=aws_ec2.InstanceType('t3.small'),
    #         # default_capacity_instance=aws_ec2.InstanceType('t3.medium'),
    #         vpc=i_vpc,
    #         masters_role=_owner_role
    #     )
    #     # CI/CDでClusterを作成する際、IAM Userでkubectlを実行する際に追加する。
    #     # kubectl commandを実行できるIAM Userを追加
    #     # _cluster.aws_auth.add_user_mapping(
    #     #         user=aws_iam.User.from_user_name(
    #     #                 self, 'K8SUser-yagitatakashi', 'yagitatakashi'),
    #     #         groups=['system:masters']
    #     # )
    #
    #     # ----------------------------------------------------------
    #     # AWS LoadBalancer Controllerをインストールする
    #     # IngressからALBを作成する。
    #     # ----------------------------------------------------------
    #     self.deploy_aws_load_balancer_controller()
    #
    #     # ----------------------------------------------------------
    #     # ExternalDNS
    #     # ExternalDNSは TLS証明書持つALBのレコードをR53に登録する
    #     # ----------------------------------------------------------
    #     self.deploy_external_dns()
    #
    #     # ----------------------------------------------------------
    #     # Cloudwatch Container Insights - Metrics / CloudWatch Agent
    #     # ----------------------------------------------------------
    #     self.deploy_cloudwatch_container_insights_metrics()
    #
    #     # ----------------------------------------------------------
    #     # Cloudwatch Container Insights - Logs / fluentbit
    #     # ----------------------------------------------------------
    #     self.deploy_cloudwatch_container_insights_logs()
    #
    #     return

    # def deploy_aws_load_balancer_controller(self):
    #     # ----------------------------------------------------------
    #     # AWS LoadBalancer Controller for AWS ALB
    #     #   - Service Account
    #     #   - Namespace: kube-system
    #     #   - Deployment
    #     #   - Service
    #     # ----------------------------------------------------------
    #     _cluster = self.resources.get('cluster')
    #     awslbcontroller_sa = _cluster.add_service_account(
    #         'LBControllerServiceAccount',
    #         name='aws-load-balancer-controller',  # fixed name
    #         namespace='kube-system',
    #     )
    #
    #     statements = []
    #     with open('./policies/awslbcontroller-policy.json') as f:
    #         data = json.load(f)
    #         for statement in data['Statement']:
    #             statements.append(aws_iam.PolicyStatement.from_json(statement))
    #
    #     policy = aws_iam.Policy(
    #         self, 'AWSLoadBalancerControllerIAMPolicy', statements=statements)
    #     policy.attach_to_role(awslbcontroller_sa.role)
    #
    #     vpc = self.resources.get('vpc')
    #
    #     aws_lb_controller_chart = _cluster.add_helm_chart(
    #         'AwsLoadBalancerController',
    #         chart='aws-load-balancer-controller',
    #         release='aws-load-balancer-controller',  # Deploymentの名前になる。
    #         repository='https://aws.github.io/eks-charts',
    #         version=None,
    #         namespace='kube-system',
    #         create_namespace=False,
    #         values={
    #             'clusterName': _cluster.cluster_name,
    #             # 'region': self.region,
    #             # 'vpcId': vpc.vpc_id,
    #             'serviceAccount': {
    #                 'name': awslbcontroller_sa.service_account_name,
    #                 'create': False,
    #                 'annotations': {
    #                     'eks.amazonaws.com/role-arn': awslbcontroller_sa.role.role_arn
    #                 }
    #             }
    #         }
    #     )
    #     aws_lb_controller_chart.node.add_dependency(awslbcontroller_sa)

    # def deploy_external_dns(self):
    #     # External DNS Controller
    #     #
    #     # External DNS Controller sets A-Record in the Hosted Zone of Route 53.
    #     #
    #     # how to use:
    #     #   Set DomainName in annotations of Ingress Manifest.
    #     #   ex.
    #     #       external-dns.alpha.kubernetes.io/hostname: DOMAIN_NAME
    #     # see more info
    #     #   ('https://aws.amazon.com/jp/premiumsupport/'
    #     #    'knowledge-center/eks-set-up-externaldns/')
    #
    #     _cluster = self.resources.get('cluster')
    #     external_dns_service_account = _cluster.add_service_account(
    #         'external-dns',
    #         name='external-dns',
    #         namespace='kube-system'
    #     )
    #     external_dns_policy_statement_json_1 = {
    #         'Effect': 'Allow',
    #         'Action': [
    #             'route53:ChangeResourceRecordSets'
    #         ],
    #         'Resource': [
    #             'arn:aws:route53:::hostedzone/*'
    #         ]
    #     }
    #
    #     external_dns_policy_statement_json_2 = {
    #         'Effect': 'Allow',
    #         'Action': [
    #             'route53:ListHostedZones',
    #             'route53:ListResourceRecordSets'
    #         ],
    #         'Resource': ["*"]
    #     }
    #
    #     external_dns_service_account.add_to_principal_policy(
    #         aws_iam.PolicyStatement.from_json(
    #             external_dns_policy_statement_json_1)
    #     )
    #     external_dns_service_account.add_to_principal_policy(
    #         aws_iam.PolicyStatement.from_json(
    #             external_dns_policy_statement_json_2)
    #     )
    #
    #     external_dns_chart = _cluster.add_helm_chart(
    #         'external-dns"',
    #         chart='external-dns',
    #         version='1.7.1',  # change to '1.9.0'
    #         # version=None,
    #         release='externaldns',
    #         repository='https://kubernetes-sigs.github.io/external-dns/',
    #         namespace='kube-system',
    #         values={
    #             'serviceAccount': {
    #                 'name': external_dns_service_account.service_account_name,
    #                 'create': False,
    #             },
    #             # 'resources': {
    #             #     'requests': {
    #             #         'cpu': '0.25',
    #             #         'memory': '0.5Gi'
    #             #     }
    #             # }
    #         }
    #
    #     )
    #     external_dns_chart.node.add_dependency(external_dns_service_account)
    #
    # def deploy_cloudwatch_container_insights_metrics(self):
    #     # CloudWatch Agent
    #     # namespace: amazon-cloudwatch -> kube-system
    #     # See more info 'https://docs.aws.amazon.com/AmazonCloudWatch/latest'
    #     #               'monitoring/Container-Insights-setup-metrics.html'
    #
    #     _cluster: aws_eks.Cluster = self.resources.get('cluster')
    #
    #     # Create the Service Account
    #     cloudwatch_container_insight_sa: aws_iam.Role = \
    #         _cluster.add_service_account(
    #             id='cloudwatch-agent',
    #             name='cloudwatch-agent',
    #             namespace='kube-system',
    #         )
    #
    #     cloudwatch_container_insight_sa.role.add_managed_policy(
    #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(
    #             'CloudWatchAgentServerPolicy')
    #     )
    #
    #     # ----------------------------------------------------------
    #     # CloudWatch ConfigMap Setting
    #     # ----------------------------------------------------------
    #     cwagentconfig_json = {
    #         'agent': {
    #             'region': self.region
    #         },
    #         'logs': {
    #             'metrics_collected': {
    #                 'kubernetes': {
    #                     'cluster_name': _cluster.cluster_name,
    #                     'metrics_collection_interval': 60
    #                 }
    #             },
    #             'force_flush_interval': 5,
    #             'endpoint_override': f'logs.{self.region}.amazonaws.com'
    #         },
    #         'metrics': {
    #             'metrics_collected': {
    #                 'statsd': {
    #                     'service_address': ':8125'
    #                 }
    #             }
    #         }
    #     }
    #     cw_agent_configmap = {
    #         'apiVersion': 'v1',
    #         'kind': 'ConfigMap',
    #         'metadata': {
    #             'name': 'cwagentconfig',
    #             'namespace': 'kube-system'
    #         },
    #         'data': {
    #             'cwagentconfig.json': json.dumps(cwagentconfig_json)
    #         }
    #     }
    #     _cluster.add_manifest('CloudwatchContainerInsightConfigMap',
    #                           cw_agent_configmap)
    #
    #     # ----------------------------------------------------------
    #     # Apply multiple yaml documents. - cloudwatch-agent.yaml
    #     # ----------------------------------------------------------
    #     with open('./manifests/cloudwatch-agent.yaml', 'r') as f:
    #         _yaml_docs = list(yaml.load_all(f, Loader=yaml.FullLoader))
    #     for i, _yaml_doc in enumerate(_yaml_docs, 1):
    #         _cluster.add_manifest(f'CWAgent{i}', _yaml_doc)
    #
    # def deploy_cloudwatch_container_insights_logs(self):
    #     # --------------------------------------------------------------
    #     # Cloudwatch Logs - fluent bit
    #     #   Namespace
    #     #   Service Account
    #     #   Deployment
    #     #   Service
    #     # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs-FluentBit.html
    #     # 1. namespace: amazon-cloudwatchを作成
    #     # 2. Service Account作成
    #     # --------------------------------------------------------------
    #
    #     _cluster = self.resources.get('cluster')
    #     # namespace: amazon-cloudwatch
    #     cloudwatch_namespace_name = 'amazon-cloudwatch'
    #     cloudwatch_namespace_manifest = {
    #         'apiVersion': 'v1',
    #         'kind': 'Namespace',
    #         'metadata': {
    #             'name': cloudwatch_namespace_name,
    #             'labels': {
    #                 'name': cloudwatch_namespace_name
    #             }
    #         }
    #     }
    #     cloudwatch_namespace = _cluster.add_manifest(
    #               'CloudWatchNamespace', cloudwatch_namespace_manifest)
    #
    #     # Service Account for fluent bit
    #     fluentbit_service_account = _cluster.add_service_account(
    #         'FluentbitServiceAccount',
    #         name='cloudwatch-sa',
    #         namespace=cloudwatch_namespace_name
    #     )
    #     fluentbit_service_account.node.add_dependency(cloudwatch_namespace)
    #     # FluentBitの場合は以下のPolicyを使う。kinesisなどを使う場合はPolicyは異なる
    #     fluentbit_service_account.role.add_managed_policy(
    #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(
    #             'CloudWatchAgentServerPolicy')
    #     )
    #     # logsの保持期間(logRetentionDays)の変更ポリシーを追加
    #     logs_retention_policy = {
    #         'Effect': 'Allow',
    #         'Action': [
    #             'logs:PutRetentionPolicy'
    #         ],
    #         'Resource': ["*"]
    #     }
    #     fluentbit_service_account.role.add_to_principal_policy(
    #         aws_iam.PolicyStatement.from_json(logs_retention_policy)
    #     )
    #
    #     # aws-for-fluent-bit DaemonSetのデプロイ
    #     cloudwatch_helm_chart = _cluster.add_helm_chart(
    #         'FluentBitHelmChart',
    #         namespace=cloudwatch_namespace_name,
    #         repository='https://aws.github.io/eks-charts',
    #         chart='aws-for-fluent-bit',
    #         release='aws-for-fluent-bit',
    #         version='0.1.16',
    #         values={
    #             'serviceAccount': {
    #                 'name': fluentbit_service_account.service_account_name,
    #                 'create': False
    #             },
    #             'cloudWatch': {
    #                 'enabled': True,
    #                 'match': "*",
    #                 'region': self.region,
    #                 'logGroupName': f'/aws/eks/fluentbit-cloudwatch/logs/{_cluster.cluster_name}/application',
    #                 'logStreamPrefix': 'log-',  # 'fluent-bit-'
    #                 'logRetentionDays': 7,
    #                 'autoCreateGroup': True,
    #             },
    #             'kinesis': {'enabled': False},
    #             'elasticsearch': {'enabled': False},
    #             'firehose': {'enabled': False},
    #         }
    #     )
    #     cloudwatch_helm_chart.node.add_dependency(fluentbit_service_account)
