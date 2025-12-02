import printdb.api as api
import printdb
from printdb.ctx import CommandContext
import printdb.utils as utils
from colorama import Fore

class Plugin(): #self suicide plugin :3
    configuration: printdb.configuration.Configuration = None
    PLUGIN_NAME = "Extra Commands"
    PLUGIN_AUTHOR = "moakdoge"
    PLUGIN_VERSION = "1.0.0"
    @api.chat_command("reload-plugins", description="Reloads all plugins. Use this when a script is changed.", example="reload-plugins")
    def reload(self,ctx: CommandContext):
        printdb.unload_plugins()
        printdb.load_plugins()
    
    @api.chat_command("list-plugins", description="Gives a list of every plugin.", example="list-plugins")
    def list_plugins(self,ctx: CommandContext):
        PLUGIN_DATA = {}
        for _, data in printdb.api.CHAT_COMMANDS.items():
            if not data["module"] in PLUGIN_DATA:
                PLUGIN_DATA[data["module"]] = []
            PLUGIN_DATA[data["module"]].append(data)

        for i,plugin in enumerate(printdb.PLUGIN_MODULES):
            p=api.get_plugin_from_command(PLUGIN_DATA[plugin][-1])
            lines = [
                f"[{api.highlight(str(i), Fore.GREEN)}]: {api.highlight(p.PLUGIN_NAME, Fore.CYAN)}",
                f"\t{api.highlight("ID:")} {plugin}",
                f"\t{api.highlight("Author:")} {p.PLUGIN_AUTHOR}",
                f"\t{api.highlight("Version:")} {p.PLUGIN_VERSION}",
                f"\t{api.highlight("Total:")} {len(PLUGIN_DATA[plugin])} commands"

            ]
            ctx.output.write("\n".join(lines))

    @api.chat_command("test-exception", description="Tests exception messages.", example="test-exception", is_debug=True)
    def test(self,ctx: CommandContext):
        raise ValueError("Test exception")

    @api.chat_command("alias", description="Keybinds a command to another command.", example='alias exit "close"',required_args=2)
    def alias(self,ctx: CommandContext):
        if not utils.validate_alias(ctx.args[0]):
            ctx.output.write(api.highlight("Please only use alphanumeric characters in your alias."))
            return
        if ctx.args[0] in api.ALIASES.keys():
            overwrite = ctx.confirm(f"Do you want to overwrite alias {ctx.args[0]}?", preferred=False)
            if not overwrite:
                ctx.output.write("Cancelled overwrite.")
                return
        api.register_alias(ctx.args[1], ctx.args[0])
        ctx.output.write("Wrote alias successfully.")
    
    @api.chat_command("save-data", description="Saves the data to the local plugin save file.", example="save-data key value", required_args=2, is_debug=True)
    def save_data(self, ctx: CommandContext):
        setattr(self.configuration, ctx.args[0],ctx.args[1])
        self.configuration.save_save()
        ctx.output.write(self.configuration._data)

    @api.chat_command("load-data", description="Reads all data saved in the configuration file.", example="load-data", required_args=0, is_debug=True)
    def load_data(self, ctx: CommandContext):
        self.configuration.load_save()
        ctx.output.write(self.configuration._data)