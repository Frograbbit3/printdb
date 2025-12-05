from . import api, configuration,plugin_manager

def init():
    api.init()
    plugin_manager.load_plugins()