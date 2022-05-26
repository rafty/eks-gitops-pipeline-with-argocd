from constructs import Construct
from util.configure.config_vpc import ConfigVpc
from util.configure.config_eks import ConfigEks
from util.configure.config_env import ConfigEnv
from util.configure.config_gitops import ConfigArgocd


class Config(Construct):

    def __init__(self, scope: Construct, id: str, sys_env: str) -> None:
        super().__init__(scope, id)

        self.sys_env = sys_env  # dev/stg/prd/ops/gitops

        self.env_config = self.node.try_get_context(key=sys_env)  # dev/stg/prd/ops/gitops

        if not self.env_config:
            # todo: The following is for debugging of debugger
            # sys_env: dev
            if 'dev' in sys_env:
                self.env_config = {
                    "env": {
                        "name": "dev"
                    },
                    "eks": {
                        "name": "app_eks",
                        "instance_type": "t3.small"
                    },
                    "vpc": {
                        "name": "gitops_pipeline"
                    }
                }
            # sys_env: gitops
            if 'gitops' in sys_env:
                self.env_config = {
                  "env": {
                      "name": "gitops"
                  },
                  "eks": {
                      "name": "gitops_eks",
                      "instance_type": "t3.medium"
                  },
                  "vpc": {
                      "name": "gitops_pipeline"
                  },
                  "argocd": {
                    "name": "argocd"
                  }
                }

    @property
    def env(self):
        if not self.env_config.get('env'):
            raise
        return ConfigEnv(self.env_config['env'])

    @property
    def vpc(self):
        if not self.env_config.get('vpc'):
            raise
        return ConfigVpc(self.env_config['vpc'])

    @property
    def eks(self):
        if not self.env_config.get('eks'):
            raise
        return ConfigEks(self.env_config['eks'])

    @property
    def argocd(self):
        if not self.env_config.get('argocd'):
            raise
        return ConfigArgocd(self.env_config['argocd'])