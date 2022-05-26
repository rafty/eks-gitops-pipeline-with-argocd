class ConfigEks:

    def __init__(self, config) -> None:
        self.config = config

    @property
    def name(self):
        return self.config['name']

    @property
    def instance_type(self):
        return self.config['instance_type']
