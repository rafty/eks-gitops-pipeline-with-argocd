class ConfigEnv:

    def __init__(self, config_env) -> None:
        self._config_env = config_env
        self._region = ''
        self._account = ''

    @property
    def name(self):
        return self._config_env['name']

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value
