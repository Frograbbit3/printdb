from printdb.api import *
import printdb

class Plugin(): #self suicide plugin :3
    @chat_command("reload-plugins", description="Reloads all plugins. Use this when a script is changed.", example="reload-plugins")
    def reload(args):
        printdb.unload_plugins()
        printdb.load_plugins()
    
    @chat_command("test-exception", description="Tests exception messages.", example="test-exception", is_debug=True)
    def test(args):
        raise ValueError("Test exception")