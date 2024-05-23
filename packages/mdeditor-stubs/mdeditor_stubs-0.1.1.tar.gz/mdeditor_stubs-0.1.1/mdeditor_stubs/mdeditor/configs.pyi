from _typeshed import Incomplete

DEFAULT_CONFIG: Incomplete

class MDConfig(dict):
    def __init__(self, config_name: str = 'default') -> None: ...
    def set_configs(self, config_name: str = 'default') -> None: ...
