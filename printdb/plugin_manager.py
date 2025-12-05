import importlib
import pkgutil
from printdb import configuration, utils
import printdb
import printdb.base_plugin


PLUGINS = []
PLUGIN_MODULES = []
CORE_PLUGINS = [
    "printdb.plugins.essential.core_plugin"
]
REGISTERED_PLUGINS: printdb.base_plugin.BasePlugin= []

def get_plugins() -> list:
    return PLUGINS

def load_plugin(mod):
    global PLUGIN_MODULES
    PLUGIN_MODULES.append(mod.__name__)

def register_plugin(**meta):
    global REGISTERED_PLUGINS
    def wrap(cls):
        global REGISTERED_PLUGINS
        cls._plugin_meta = meta
        REGISTERED_PLUGINS.append(cls)
        return cls
    return wrap

def load_plugins():
    global PLUGINS, PLUGIN_MODULES
    c=0
    for plg in CORE_PLUGINS:
        load_plugin(importlib.import_module(plg))
        c+=1

    for _, module_name, _ in pkgutil.iter_modules(printdb.plugins.__path__):
        full = f"printdb.plugins.{module_name}"
        m = importlib.import_module(full)
        utils.create_folder(configuration.SAVE_FOLDER)
        utils.create_folder(utils.path_join(configuration.SAVE_FOLDER, "plugins"))
        load_plugin(m)
        c += 1
    for cls in REGISTERED_PLUGINS:
        name = cls._plugin_meta

        instance = cls()
        p=f"plugins/%s.json" % instance.META.id
        instance.configuration = configuration.Configuration(p)
        instance.configuration.load_save()
        instance.on_load()
        PLUGINS.append(instance)


def unload_plugin(plugin_modname: str):
    global PLUGINS, PLUGIN_MODULES, REGISTERED_PLUGINS
    from printdb.api import CHAT_COMMANDS
    import sys

    if plugin_modname in CORE_PLUGINS:
        return
    
    for key, data in list(CHAT_COMMANDS.items()):
        if data["module"] == plugin_modname:
            del CHAT_COMMANDS[key]

    for mod in list(sys.modules.keys()):
        if mod == plugin_modname or mod.startswith(plugin_modname + "."):
            del sys.modules[mod]

    PLUGINS = [p for p in PLUGINS if p.__class__.__module__ != plugin_modname]

    PLUGIN_MODULES = [m for m in PLUGIN_MODULES if m != plugin_modname]


    REGISTERED_PLUGINS = [
        cls for cls in REGISTERED_PLUGINS
        if cls.__module__ != plugin_modname
    ]

def unload_plugins():
    global PLUGINS, PLUGIN_MODULES
    from printdb.api import CHAT_COMMANDS

    for mod in PLUGIN_MODULES:
        unload_plugin(mod)

    