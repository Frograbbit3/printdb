from pathlib import *
import sys
from colorama import Fore

import printdb
from printdb.api import *
from printdb.plugin_api import *
from datetime import datetime
@register_plugin()
class Plugin(printdb.base_plugin.BasePlugin):
    META = printdb.base_plugin.PluginMeta(
        "Core",
        "moakdoge",
        "1.0.0",
        "The core commands.",
        "core.commands"
    )
    @chat_command("welcome", description="Welcomes the user.", example="welcome")
    def welcome(self, ctx: CommandContext):
        def newline():
            return "\n"

        runtime = time.time() - api.START_TIME
        def fmt_time(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = sec % 60
            return f"{h:02}:{m:02}:{s:05.2f}"
        lines = [
            f"Welcome, @{highlight(username())}!",
            f"Today is {datetime.now().strftime(f"{highlight("%Y/%m/%d", Fore.CYAN)} {highlight("and it's currently", Fore.WHITE)} {highlight("%H:%M:%S", Fore.CYAN)}")}",
            f"Currently, there are {highlight(len(CHAT_COMMANDS.keys()), Fore.YELLOW)} commands loaded,",
            f"split across {highlight(len(plugin_manager.PLUGINS))} total plugins.",
            "[dash]",
            f"You are currently logged into UID {highlight(os.getuid(), Fore.GREEN)}",
            f"Aliases: {highlight(len(ALIASES), Fore.MAGENTA)}",
            f"Sandbox mode: {highlight('ON', Fore.GREEN) if api.CONFIGURATION.sandboxed else highlight('OFF', Fore.RED)}",
            f"Uptime: {highlight(fmt_time(runtime))}",
            "[dash]",
            f"Thanks for using {highlight("printdb!", Fore.LIGHTYELLOW_EX)}"
        ]
        real_lines = []
        max_len = 0
        ANSI = re.compile(r'\x1b\[[0-9;]*m')


        
        for line in lines:
            if max_len < len(line):
                max_len = len(line)
        real_lines.append((max_len+4) * "-")
        for l in lines:
            f=ANSI.sub("", l)
            if len(f) % 2 != 0:
                l+=" "
            if f == "\n":
                l = ""
                SPACES = max_len
            elif f == "[dash]":
                real_lines.append("||" + ("-" * ((max_len))) + "||")
                continue
            else:
                SPACES = max_len - len(f)
            real_lines.append(f"||{" " * (SPACES//2)}{l}{" " * (SPACES//2)}||")
        real_lines.append((max_len+4) * "-")
        ctx.output.write("\n".join(real_lines))

    @chat_command("help", description="Gets command info",example="help ls")
    def help(self,ctx):
        args=ctx.args
        if len(args) > 1:
            ctx.output.write(highlight("[ALL COMMANDS]", Fore.BLUE))
            ctx.output.write(f"Total:  {len(CHAT_COMMANDS.keys())}")
        sorted_plugins = {}
        for command, details in CHAT_COMMANDS.items():
            if len(args) > 0:
                if command != args[0]:
                    continue
                if details["hidden"] == True:
                    continue
            if getattr(get_plugin_from_command(details), "HIDDEN", False):
                continue
            if details["module"] not in sorted_plugins:
                sorted_plugins[details["module"]] = []
            details["command"] = command
            sorted_plugins[details["module"]].append(details)

        for module, funcs in sorted_plugins.items():
            p=get_plugin_from_command(funcs[0])
            if getattr(p, "HIDDEN", False):
                continue
            ctx.output.write(f"{highlight(get_plugin_stats(p)["name"], Fore.GREEN)}:")
            for details in funcs:
                if details["hidden"] == True:
                    continue
                ctx.output.write(f"\t{highlight(details["command"], Fore.BLUE)} : {highlight(details["description"], Fore.RED)} ({details["example"]}) {highlight("[DEBUG ONLY]", Fore.CYAN) if details["debug"] else ""} {highlight("[SANDBOXED]", Fore.YELLOW) if details["sandboxed"] else ""}")
    @chat_command("cat", description="Reads the contents of a file.", example="cat file.txt")
    def cat(self,ctx):
        args = ctx.args

        # CASE 1: files specified
        if len(args) > 0:
            for path in args:
                if path == "-":  # meaning stdin
                    if ctx.input is None:
                        error("cat: no input provided for '-'")
                    else:
                        ctx.output.write(ctx.input.read())
                    continue

                full = os.path.abspath(path)
                if not os.path.exists(full):
                    error(f"cat: {path}: No such file")
                    continue

                with open(full, "r") as f:
                    ctx.output.write(f.read())

            return  # done

        # CASE 2: no args → use stdin
        if ctx.input:
            ctx.output.write(ctx.input.read())
        else:
            error("cat: no input")


    @chat_command("ls", description="Gets the files in the current directory", example="ls")
    def ls(self,ctx):
        args=ctx.args
        if len(args) > 0:
            PATH = expand_path(args[0])
        else:
            PATH=os.getcwd()
        _FILES = os.listdir(PATH)
        for c, fi in enumerate(_FILES):
            if os.path.isdir(fi):
                if fi.startswith(".") and not "-f" in args:
                    continue
                
                ctx.output.write(f"\t{fi} {" " * (80-len(fi)-4)}[folder]")
        for fi in _FILES:
            if os.path.isfile(fi):
                if fi.startswith(".") and not "-f" in args:
                    continue
                ctx.output.write(f"\t{fi}{" " * (80-len(fi)-4)} [file]")

    @chat_command("echo", description="Echos text into output.", example="echo hello, world!")
    def echo(self,ctx):
        args=ctx.args
        fixed = " ".join(args)
        ctx.output.write(fixed)
        

    @chat_command("wait", description="Waits for n seconds.", example="wait 10", required_args=1)
    def wait(self,ctx):
        args=ctx.args
        time.sleep(float(args[0]))

    @chat_command("cd", description="Changes directory.", example="cd ..", required_args=1)
    def cd(self,ctx):
        args=ctx.args
        path = expand_path(args[0])
        if not os.path.exists(path):
            error(f"{path} does not exist!")
            return
        change_path(path)

    @chat_command("grep", description="Search for a pattern in input or files.", example="grep pattern file.txt", required_args=1)
    def grep(self,ctx):
        args = ctx.args

        # PATTERN is always the first argument
        pattern = args[0]
        if len(args) > 1:
            files = args[1:]
            for fname in files:
                if not os.path.exists(fname):
                    error(f"grep: {fname}: No such file")
                    continue

                with open(fname, "r") as f:
                    for line in f.readlines():
                        if pattern in line:
                            ctx.output.write(line.rstrip("\n"))
            return

        if ctx.input:
            data = ctx.input.read().splitlines()
            for line in data:
                if pattern in line:
                    line=line.replace(pattern,highlight(pattern,color=Fore.CYAN))
                    ctx.output.write(line)
            return

        # No files and no stdin
        error("grep: no input")

    @chat_command("exit", "Quits the terminal.", example="exit")
    def close(self,ctx):
        sys.exit(1)


