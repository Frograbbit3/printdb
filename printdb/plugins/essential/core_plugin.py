from colorama import Fore
from printdb.plugin_api import *
@register_plugin()
class Plugin(base.BasePlugin):
    META = base.PluginMeta(
        "Essential Commands",
        "moakdoge",
        "1.0.0",
        "A plugin with strictly reload-plugin commands. (NOTE - THIS CANNOT BE UNLOADED!)",
        hidden=True
    )
    
    @api.chat_command("unload-plugins", description="Goodbye, world! Unloads all loaded plugins. (You can recover by calling load-plugins!)", example="unload-plugins", is_debug=True)
    def suicide(a,b: CommandContext): #eheh
        plugin_manager.unload_plugins()
        b.output.write(api.highlight("Unloaded plugins. [Note -- You can load plugins back using load-plugins.]"))

    @api.chat_command("load-plugins", description="Loads all plugins. ONLY USE IF UNLOAD-PLUGINS IS CALLED", example="load-plugins")
    def reload(self,ctx: CommandContext):
        plugin_manager.load_plugins()
    