import printdb.api as api
import printdb
from printdb.ctx import CommandContext
import printdb.utils as utils
import printdb.configuration as conf
import printdb.cross_platform.processes as ProcessManager
import printdb.base_plugin as base
import time
from printdb.plugin_api import *
from colorama import Fore

@printdb.plugin_manager.register_plugin()
class Plugin(base.BasePlugin): #self suicide plugin :3
    META = base.PluginMeta(
        "Debug",
        "moakdoge",
        "de.bu.gg.er",
        "Plugins to help debug the engine. These are normally hidden when debug is off.",
        "core.debug"
    )


    def __init__(self):
        pass

    @api.chat_command("test-exception", description="Tests exception messages.", example="test-exception", is_debug=True)
    def test(self,ctx: CommandContext):
        raise ValueError("Test exception")
    
    @api.chat_command("save-data", description="Saves the data to the local plugin save file.", example="save-data key value", required_args=2, is_debug=True)
    def save_data(self, ctx: CommandContext, key: str, val: str):
        setattr(self.configuration, key, val)
        self.configuration.save_save()
        ctx.output.write(self.configuration._data)

    @api.chat_command("load-data", description="Reads all data saved in the configuration file.", example="load-data", required_args=0, is_debug=True)
    def load_data(self, ctx: CommandContext):
        self.configuration.load_save()
        ctx.output.write(self.configuration._data)

    @api.chat_command("open-config-folder", description="Opens the configuration folder inside your default file explorer.", example="open-config-folder", required_args=0, is_debug=True)
    def open_config_folder(self, ctx: CommandContext):
        utils.open_file(conf.SAVE_FOLDER)

    @api.chat_command("run", description="Runs an executable. Supports args", example="run kcalc", required_args=1, is_debug=True, is_sandboxed=True)
    def run(self, ctx:CommandContext):
        m = ProcessManager.Process(ctx.args[0], ctx.args[1::])
        m.run()
        m.block()
        print(m.return_code)
    
    @api.chat_command("test-formatting", 
                      description="Tests the formatting system. Uses tags for colors.", 
                      example="test-formatting [[red]]This is red text!", 
                      is_debug=True)
    def test_formatting(self, ctx:CommandContext):
        ctx.output.write(ansi_format(" ".join(ctx.args)))

    @api.chat_command("test-args", description="Tests argument types.",example="test-args 0", is_debug=True)
    def test_args(self, ctx:CommandContext, arg1: float, arg2: int = 0):
        for i,arg in enumerate(ctx.args):
            ctx.output.write(ansi_format(f"[[red]]Arg {i}:[[reset]] {arg} [[green]]Type:{type(arg)}[[reset]]"))