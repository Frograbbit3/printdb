import printdb.api
import importlib
import pkgutil
from printdb import plugins, configuration, utils

PLUGINS = []
PLUGIN_MODULES = []
CORE_PLUGINS = [
    "printdb.core_plugin"
]
def load_plugin(mod):
    global PLUGIN_MODULES
    PLUGIN_MODULES.append(mod.__name__)
    instance = mod.Plugin()
    instance.configuration = configuration.Configuration(f"plugins/{mod}")
    instance.configuration.load_save()
    PLUGINS.append(instance)
    
def load_plugins():
    global PLUGINS, PLUGIN_MODULES
    c=0
    for plg in CORE_PLUGINS:
        load_plugin(importlib.import_module(plg))
        c+=1

    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        full = f"printdb.plugins.{module_name}"
        m = importlib.import_module(full)
       
        utils.create_folder(configuration.SAVE_FOLDER)
        utils.create_folder(utils.path_join(configuration.SAVE_FOLDER, "plugins"))
        load_plugin(m)

        c += 1
    
    printdb.api.log(f"Loaded {c} plugins successfully")


def unload_plugins(a=None,b=None):
    global PLUGINS, PLUGIN_MODULES
    from printdb.api import CHAT_COMMANDS


    for key in list(CHAT_COMMANDS.keys()):
        module = CHAT_COMMANDS[key].get("module")
        if module in CORE_PLUGINS:
            continue
        if module in PLUGIN_MODULES:
            del CHAT_COMMANDS[key]

    import sys
    for module in PLUGIN_MODULES:
        if module in CORE_PLUGINS:
            continue
        if module in sys.modules:
            del sys.modules[module]
    PLUGINS = [p for p in PLUGINS if p.__class__.__module__ in CORE_PLUGINS]
    PLUGIN_MODULES = [p for p in PLUGIN_MODULES if p in CORE_PLUGINS]
    