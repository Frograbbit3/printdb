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
            f"Welcome, @{highlight(get_username())}!",
            f"Today is {datetime.now().strftime(f"{highlight("%Y/%m/%d", Fore.CYAN)} {highlight("and it's currently", Fore.WHITE)} {highlight("%H:%M:%S", Fore.CYAN)}")}",
            f"Currently, there are {highlight(len(CHAT_COMMANDS.keys()), Fore.YELLOW)} commands loaded,",
            f"split across {highlight(len(plugin_manager.PLUGINS))} total plugins.",
            "[dash]",
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
    def help(self,ctx, cmd:str = ""):
        if cmd is None:
            ctx.output.write("[[blue]][[bold]]ALL COMMANDS")
            ctx.output.write(f"Total:  {len(CHAT_COMMANDS.keys())}")
        sorted_plugins = {}
        for command, details in CHAT_COMMANDS.items():
            if cmd is None:
                if command != cmd:
                    continue
                if details["hidden"] == True:
                    continue
            if get_plugin_from_command(details).META.hidden:
                continue
            if details["module"] not in sorted_plugins:
                sorted_plugins[details["module"]] = []
            details["command"] = command
            sorted_plugins[details["module"]].append(details)

        for module, funcs in sorted_plugins.items():
            p=get_plugin_from_command(funcs[0])
            if getattr(p, "HIDDEN", False):
                continue
            ctx.output.write(f"[[green]] {get_plugin_stats(p)["name"]}:")
            for details in funcs:
                if details["hidden"] == True:
                    continue
                args = get_args(details["command"])
                prmp = ""
                if args is not None:
                    for arg, dd in args.items():
                        prmp += f"[[cyan]]{arg}: [[red]]{dd["type"]}"
                        if dd["optional"]:
                            prmp += " (optional)"
                        prmp += ", "
                de= [
                   f"\t[[red]][[bold]]{details["command"]}: [[reset]][[yellow]]{prmp}[[reset]]",
                   f"\t\t[[blue]]{details["description"]}[[reset]]",
                   f"\t\t[[green]]Usage: '{details["example"]}[[green]]'[[reset]]",
                   f"\t\t[[yellow]]{"[SANDBOXED]" if details["sandboxed"] else ""}[[cyan]]{"[DEBUG]" if details["debug"] else ""}",
                ]
                ctx.output.write("\n".join(de))
                #ctx.output.write(f"\t{highlight(details["command"], Fore.BLUE)} : {highlight(details["description"], Fore.RED)} ({details["example"]}) {highlight("[DEBUG ONLY]", Fore.CYAN) if details["debug"] else ""} {highlight("[SANDBOXED]", Fore.YELLOW) if details["sandboxed"] else ""}")
    
    @chat_command("cat", description="Reads the contents of a file.", example="cat file.txt")
    def cat(self,ctx: CommandContext, file: Path):
        content = ""
        if file is not None:
            if file.is_file():
                with open(file, "r") as m:
                    content=m.read()
            else:
                ctx.output.write("[[red]]Please provide a file, not a directory. ")
        ctx.output.write(content)

         


    @chat_command("ls", description="Gets the files in a directory.", example="ls ~")
    def ls(self, ctx, path: Path=None, force: bool = False):
        if path is not None:
            
            _FILES = os.listdir(path.absolute())
            f = path.absolute()
        else:
            _FILES=  os.listdir(os.getcwd())
            f = os.getcwd()
        k=[]
        for c, fi in enumerate(_FILES):
            if os.path.isdir(os.path.join(f,fi)):
                if fi.startswith(".") and not force:
                    continue
                
                k.append(pad_string(ansi_format(f"[[red]][[bold]]{fi}[[reset]]"), 80, align="left", left_padding=5))

        for c, fi in enumerate(_FILES):
            if fi.startswith(".") and not force:
                    continue
            if os.path.isfile(os.path.join(f,fi)):
               k.append(pad_string(ansi_format(f"{fi}"), 80, align="left", left_padding=5))
        ctx.output.write(columnize(k))

    @chat_command("echo", description="Echos text into output.", example="echo hello, world!")
    def echo(self,ctx: CommandContext): #bad example lol
        fixed = ctx.full_command.lstrip("echo").lstrip()
        ctx.output.write(fixed)
        

    @chat_command("wait", description="Waits for n seconds.", example="wait 10", required_args=1)
    def wait(self,ctx, seconds: float):
        time.sleep(seconds)

    @chat_command("cd", description="Changes directory.", example="cd ..", required_args=1)
    def cd(self,ctx: CommandContext, path: Path):
        change_path(path.absolute())

    @chat_command("grep", description="Search for a pattern in input or files.", example="grep pattern file.txt", required_args=1)
    def grep(self,ctx:CommandContext, pattern: str, file:Path = None, input:str = ""):
        lines: list[str] = []
        if file is not None:
            with open(file, "r") as f:
                lines = f.read().splitlines()
        elif input is not None:
            lines = input.splitlines()
        elif ctx.input.read() != "":
            lines = ctx.input.read().splitlines()

        results = 0
        for line in lines:
            if pattern in line:
                ctx.output.write(ansi_format(f"{line.replace(pattern, f"[[red]]{pattern}[[reset]]")}"))
                results+=1
        if results < 1:
            ctx.output.write(ansi_format("[[red]]grep: no results found"))

    @chat_command("exit", "Quits the terminal.", example="exit")
    def close(self,ctx: CommandContext, exit_code: int = 1):
        sys.exit(exit_code)


