from constructs import Construct
from aws_cdk import aws_eks
from aws_cdk import aws_ec2
from aws_cdk import aws_iam
from util.configure.config import Config
from _constructs.eks_awslbctl_addon import AwsLoadBalancerController
from _constructs.eks_extdns_addon import ExternalDnsController
from _constructs.eks_cw_metrics_addon import CloudWatchContainerInsightsMetrics
from _constructs.eks_cw_logs_addon import CloudWatchContainerInsightsLogs


class EksCluster(Construct):
    # --------------------------------------------------------------
    # EKS Cluster
    # --------------------------------------------------------------
    def __init__(self, scope: Construct, id: str, config: Config) -> None:
        super().__init__(scope, id)

        self.config = config
        self.cluster = None

    def provisioning(self):
        i_vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_name=self.config.vpc.name)

        _owner_role = aws_iam.Role(
            scope=self,
            id='EksClusterOwnerRole',
            role_name=f'{self.config.env.name}EksClusterOwnerRole',
            assumed_by=aws_iam.AccountRootPrincipal())

        self.cluster = aws_eks.Cluster(
            self,
            'EksCluster',
            cluster_name=self.config.eks.name,
            version=aws_eks.KubernetesVersion.V1_21,
            default_capacity_type=aws_eks.DefaultCapacityType.NODEGROUP,
            default_capacity=1,
            default_capacity_instance=aws_ec2.InstanceType(self.config.eks.instance_type),
            vpc=i_vpc,
            masters_role=_owner_role)

        # CI/CDでClusterを作成する際、IAM Userでkubectlを実行する際に追加する。
        # kubectl commandを実行できるIAM Userを追加
        # self.cluster.aws_auth.add_user_mapping(
        #         user=aws_iam.User.from_user_name(
        #                 self, 'K8SUser-yagitatakashi', 'yagitatakashi'),
        #         groups=['system:masters']
        # )

        # ------------------------------------------------
        # EKS Add On
        #   - AWS Load Balancer Controller
        #   - External DNS
        #   - CloudWatch Container Insight Metrics
        #   - CloudWatch Container Insight Logs
        # ------------------------------------------------
        alb_ctl = AwsLoadBalancerController(
            self,
            'AwsLbController',
            region=self.config.env.region,
            cluster=self.cluster)
        alb_ctl.deploy()

        ext_dns = ExternalDnsController(
            self,
            'ExternalDNS',
            cluster=self.cluster)
        ext_dns.deploy()

        insight_metrics = CloudWatchContainerInsightsMetrics(
            self,
            'CloudWatchInsightsMetrics',
            region=self.config.env.region,
            cluster=self.cluster)
        insight_metrics.deploy()

        insight_logs = CloudWatchContainerInsightsLogs(
            self,
            'CloudWatchInsightLogs',
            region=self.config.env.region,
            cluster=self.cluster)
        insight_logs.deploy()
