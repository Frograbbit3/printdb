import printdb.api as api
import printdb
from printdb.ctx import CommandContext
import printdb.utils as utils
import printdb.configuration as conf
import time
from colorama import Fore

class Plugin(): #self suicide plugin :3
    configuration: printdb.configuration.Configuration = None
    PLUGIN_NAME = "Debug Plugins"
    PLUGIN_AUTHOR = "moakdoge"
    PLUGIN_VERSION = "de.bu.gg.er"

    @api.chat_command("test-exception", description="Tests exception messages.", example="test-exception", is_debug=True)
    def test(self,ctx: CommandContext):
        raise ValueError("Test exception")

    
    @api.chat_command("save-data", description="Saves the data to the local plugin save file.", example="save-data key value", required_args=2, is_debug=True)
    def save_data(self, ctx: CommandContext):
        setattr(self.configuration, ctx.args[0],ctx.args[1])
        self.configuration.save_save()
        ctx.output.write(self.configuration._data)

    @api.chat_command("load-data", description="Reads all data saved in the configuration file.", example="load-data", required_args=0, is_debug=True)
    def load_data(self, ctx: CommandContext):
        self.configuration.load_save()
        ctx.output.write(self.configuration._data)

    @api.chat_command("open-config-folder", description="Opens the configuration folder inside your default file explorer.", example="open-config-folder", required_args=0, is_debug=True)
    def open_config_folder(self, ctx: CommandContext):
        utils.open_file(conf.SAVE_FOLDER)