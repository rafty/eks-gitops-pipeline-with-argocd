import json
import yaml
from constructs import Construct
from aws_cdk import aws_iam


class CloudWatchContainerInsightsMetrics(Construct):
    # ----------------------------------------------------------
    # Cloudwatch Container Insights - Metrics / CloudWatch Agent
    # ----------------------------------------------------------

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id)

        self.region = kwargs.get('region')
        self.cluster = kwargs.get('cluster')

    def deploy(self):
        # CloudWatch Agent
        # namespace: amazon-cloudwatch -> kube-system
        # See more info 'https://docs.aws.amazon.com/AmazonCloudWatch/latest'
        #               'monitoring/Container-Insights-setup-metrics.html'

        # _cluster: aws_eks.Cluster = self.resources.get('cluster')

        # Create the Service Account
        cloudwatch_container_insight_sa: aws_iam.Role = \
            self.cluster.add_service_account(
                id='cloudwatch-agent',
                name='cloudwatch-agent',
                namespace='kube-system',
            )

        cloudwatch_container_insight_sa.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                'CloudWatchAgentServerPolicy')
        )

        # ----------------------------------------------------------
        # CloudWatch ConfigMap Setting
        # ----------------------------------------------------------
        cwagentconfig_json = {
            'agent': {
                'region': self.region
            },
            'logs': {
                'metrics_collected': {
                    'kubernetes': {
                        'cluster_name': self.cluster.cluster_name,
                        'metrics_collection_interval': 60
                    }
                },
                'force_flush_interval': 5,
                'endpoint_override': f'logs.{self.region}.amazonaws.com'
            },
            'metrics': {
                'metrics_collected': {
                    'statsd': {
                        'service_address': ':8125'
                    }
                }
            }
        }
        cw_agent_configmap = {
            'apiVersion': 'v1',
            'kind': 'ConfigMap',
            'metadata': {
                'name': 'cwagentconfig',
                'namespace': 'kube-system'
            },
            'data': {
                'cwagentconfig.json': json.dumps(cwagentconfig_json)
            }
        }
        self.cluster.add_manifest(
            'CloudwatchContainerInsightConfigMap',
            cw_agent_configmap)

        # ----------------------------------------------------------
        # Apply multiple yaml documents. - cloudwatch-agent.yaml
        # ----------------------------------------------------------
        with open('./manifests/cloudwatch-agent.yaml', 'r') as f:
            _yaml_docs = list(yaml.load_all(f, Loader=yaml.FullLoader))
        for i, _yaml_doc in enumerate(_yaml_docs, 1):
            self.cluster.add_manifest(f'CWAgent{i}', _yaml_doc)
