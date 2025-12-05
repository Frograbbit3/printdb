import getpass
import printdb.plugin_manager
import printdb.base_plugin as base

def username():
    return getpass.getuser()

def get_plugin_by_id(id: str) -> base.BasePlugin:
    for plugin in printdb.plugin_manager.PLUGINS:
        if plugin.META.id == id:
            return plugin
    return None

def get_plugin_ids() -> list[str]:
    plugin_ids: list[str] = []
    for plugin in printdb.plugin_manager.PLUGINS:
        plugin_ids.append(plugin.META.id)
    return plugin_ids