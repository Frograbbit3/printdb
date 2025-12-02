import printdb.api as api
import printdb
from printdb.ctx import CommandContext
import printdb.utils as utils
from colorama import Fore

class Plugin(): #self suicide plugin :3
    configuration: printdb.configuration.Configuration = None
    @api.chat_command("reload-plugins", description="Reloads all plugins. Use this when a script is changed.", example="reload-plugins")
    def reload(ctx: CommandContext):
        printdb.unload_plugins()
        printdb.load_plugins()
    
    @api.chat_command("list-plugins", description="Gives a list of every plugin.", example="list-plugins")
    def list_plugins(ctx: CommandContext):
        PLUGIN_DATA = {}
        for _, data in printdb.api.CHAT_COMMANDS.items():
            if not data["module"] in PLUGIN_DATA:
                PLUGIN_DATA[data["module"]] = []
            PLUGIN_DATA[data["module"]].append(data)

        for i,plugin in enumerate(printdb.PLUGIN_MODULES):
            ctx.output.write(f"[{api.highlight(str(i), Fore.GREEN)}]: {api.highlight(plugin, Fore.CYAN)} (Total commands: {len(PLUGIN_DATA[plugin])})")

    @api.chat_command("test-exception", description="Tests exception messages.", example="test-exception", is_debug=True)
    def test(ctx: CommandContext):
        raise ValueError("Test exception")

    @api.chat_command("alias", description="Keybinds a command to another command.", example='alias exit "close"',required_args=2)
    def alias(ctx: CommandContext):
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