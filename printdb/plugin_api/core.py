import getpass
import printdb.plugin_manager
import printdb.base_plugin as base
ANSI_COLOR_CODES = {
    "reset": "\033[0m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bold": "\033[1m",
}


def get_username():
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

def ansi_format(st: str) -> str:
    for name, color in ANSI_COLOR_CODES.items():
        st = st.replace(f"[[{name}]]", color)
    st+=ANSI_COLOR_CODES["reset"]
    return st