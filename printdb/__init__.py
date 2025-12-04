from . import api, configuration,plugin_manager

def init():
    api.load_configuration()
    api.init()
    plugin_manager.load_plugins()