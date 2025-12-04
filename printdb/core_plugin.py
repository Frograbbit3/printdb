from colorama import Fore
import printdb
import printdb.api as api
from printdb.ctx import CommandContext

class Plugin:
    PLUGIN_NAME = "[CORE]"
    PLUGIN_VERSION = "C.O.R.E"
    PLUGIN_AUTHOR = "printdb"
    HIDDEN=True

    
    @api.chat_command("unload-plugins", description="Goodbye, world! Unloads all loaded plugins. (You can recover by calling load-plugins!)", example="unload-plugins", is_debug=True)
    def suicide(a,b: CommandContext): #eheh
        from printdb import unload_plugins
        unload_plugins()
        b.output.write(api.highlight("Unloaded plugins. [Note -- You can load plugins back using load-plugins.]"))

    @api.chat_command("load-plugins", description="Loads all plugins. ONLY USE IF UNLOAD-PLUGINS IS CALLED", example="load-plugins")
    def reload(self,ctx: CommandContext):
        printdb.load_plugins()
    