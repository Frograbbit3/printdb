import printdb.api as api
import printdb
from printdb.ctx import CommandContext
import printdb.utils as utils
from colorama import Fore
import printdb.base_plugin as base
import platform
import subprocess,re, time


@printdb.plugin_manager.register_plugin()
class Plugin(base.BasePlugin): #self suicide plugin :3
    META = base.PluginMeta(
        "Networking",
        "moakdoge",
        "1.0.0",
        "Networking commands.",
        id="core.networking"
    )
    
    @api.chat_command("ping", "Sends a ping request to a certain website. Goes until Control + C is pressed.", example="ping google.com", required_args=1)
    def ping(self,ctx:CommandContext):
        while True:
            param = "-n" if platform.system().lower()=="windows" else "-c"
            p = subprocess.run(
                ["ping", param, "1", ctx.args[0]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            out = p.stdout
            match = re.search(r"time=([\d.]+)\s*ms", out)
            ctx.output.write(f"Took: {float(match.group(1))}ms")
            time.sleep(0.25)