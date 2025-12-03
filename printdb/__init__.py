import printdb.api
import importlib
import pkgutil
from printdb import plugins, configuration, utils

PLUGINS = []
PLUGIN_MODULES = []
def load_plugins():
    global PLUGINS, PLUGIN_MODULES
    c=0
    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        full = f"printdb.plugins.{module_name}"
        m = importlib.import_module(full)
        PLUGIN_MODULES.append(full)
        utils.create_folder(configuration.SAVE_FOLDER)
        utils.create_folder(utils.path_join(configuration.SAVE_FOLDER, "plugins"))
        instance = m.Plugin()
        instance.configuration = configuration.Configuration(f"plugins/{full}")
        instance.configuration.load_save()
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