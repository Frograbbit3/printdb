from printdb.plugin_api import *
import time



@register_plugin()
class Plugin(base.BasePlugin): #self suicide plugin :3
    META = base.PluginMeta(
        "Extra",
        "moakdoge",
        "1.0.0",
        "Misc plugins that don't matter very much."
    )
    @api.chat_command("reload-plugins", description="Reloads all plugins. Use this when a script is changed.", example="reload-plugins")
    def reload(self,ctx: CommandContext):
        plugin_manager.unload_plugins()
        plugin_manager.load_plugins()
    
    @api.chat_command("list-plugins", description="Gives a list of every plugin.", example="list-plugins")
    def list_plugins(self,ctx: CommandContext):
        PLUGIN_DATA = {}
        for _, data in api.CHAT_COMMANDS.items():
            if not data["module"] in PLUGIN_DATA:
                PLUGIN_DATA[data["module"]] = []
            PLUGIN_DATA[data["module"]].append(data)

        i=0
        for k,plugin in enumerate(plugin_manager.PLUGINS):
            p=plugin
            commands = PLUGIN_DATA[plugin.__module__]
            if getattr(p.META, "HIDDEN", False):
                continue
            lines = [
                f"[{api.highlight(str(i+1), Fore.GREEN)}]: {api.highlight(p.META.name, Fore.CYAN)}",
                f"\t{api.highlight("ID:")} {plugin}",
                f"\t{api.highlight("Author:")} {p.META.author}",
                f"\t{api.highlight("Version:")} {p.META.version}",
                f"\t{api.highlight("Total:")} {len(commands)} commands",
                f"\t{api.highlight("Description:")} {p.META.description}"
                

            ]
            ctx.output.write("\n".join(lines))
            i+=1

    @api.chat_command("alias", description="Keybinds a command to another command.", example='alias close exit',required_args=2)
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
    
    @api.chat_command("list-alias", description="Lists all the aliases currently applied.", example="aliases")
    def list_aliases(self, ctx:CommandContext):
        i=0
        for alias, val in api.ALIASES.items():
            i+=1
            ctx.output.write(f"[{api.highlight(str(i), Fore.CYAN)}]: {alias} -> {val}")

    @api.chat_command("time", description="Times the length of a command.", example="time wait 20",required_args=1)
    def time(self, ctx: CommandContext):
        f=""
        new_cmd = ctx.full_command.removeprefix("time").strip()
        if ctx.output.redirect_file is not None:
            m=ctx.output.redirect_mode
            f=ctx.output.redirect_file
            ctx.output.stop_redirect()
            extra = f"m"
        else:
            extra = ""
        cmd = new_cmd
        start = time.time()
        api.send_chat_command(cmd, False)
        end = time.time()
        if extra != "":
            ctx.output.start_redirect(f,"a")
        ctx.output.write(f"Command {cmd} took {end - start:.4f}s.")