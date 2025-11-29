import printdb.api
import importlib
import pkgutil
from printdb import plugins

PLUGINS = []
PLUGIN_MODULES = []
def load_plugins():
    global PLUGINS, PLUGIN_MODULES
    c=0
    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        full = f"printdb.plugins.{module_name}"
        m = importlib.import_module(full)
        PLUGIN_MODULES.append(full)

        instance = m.Plugin()
        PLUGINS.append(instance)

        c += 1
    
    printdb.api.log(f"Loaded {c} plugins successfully")
def unload_plugins():
    global PLUGINS, PLUGIN_MODULES
    from printdb.api import CHAT_COMMANDS


    for key in list(CHAT_COMMANDS.keys()):
        module = CHAT_COMMANDS[key].get("module")
        if module in PLUGIN_MODULES:
            del CHAT_COMMANDS[key]

    import sys
    for module in PLUGIN_MODULES:
        if module in sys.modules:
            del sys.modules[module]
    PLUGINS.clear()
    PLUGIN_MODULES.clear()