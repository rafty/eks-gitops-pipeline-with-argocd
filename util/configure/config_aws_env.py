class ConfigAwsEnv:

    def __init__(self, config_aws_env) -> None:
        self._config_aws_env = config_aws_env

    @property
    def region(self):
        return self._config_aws_env.get('region')

    @property
    def account(self):
        return self._config_aws_env.get('account')
