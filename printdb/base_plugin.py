from dataclasses import dataclass
import printdb.configuration

@dataclass(frozen=True)
class PluginMeta:
    name: str = "[UKNOWN]"
    author: str = "[UNKNOWN]"
    version: str = "[UNKNOWN]"
    description: str = ""
    hidden: bool = False

class BasePlugin:
    configuration:printdb.configuration.Configuration = None
    PLUGIN_META = PluginMeta()
    def __init__(self):
        pass
    def on_load(self):
        pass
    def on_unload(self):
        pass