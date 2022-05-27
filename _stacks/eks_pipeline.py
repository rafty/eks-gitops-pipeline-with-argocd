from aws_cdk import Stack
from constructs import Construct
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

        # ---------------------------------------------------------
        # Stackの設定値をConfigに保存する。
        _env = kwargs['env']
        aws_env = {'region': _env.region, 'account': _env.account}
        self.config = Config(self, 'Config', sys_env, aws_env)

        # VPCは事前に作成してる。既存VPC名はCDK.jsonにある。
        _eks_cluster = EksCluster(self, 'EksCluster', config=self.config)
        _eks_cluster.provisioning()

        # Todo: Argo CDを ops appとしてデプロイする。
