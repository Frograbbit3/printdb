from printdb.api import *
from pathlib import *
import sys
from colorama import Fore

class Plugin():
    @chat_command("help", description="Gets command info",example="help ls")
    def help(ctx):
        args=ctx.args
        if len(args) > 1:
            ctx.output.write(highlight("[ALL COMMANDS]", Fore.BLUE))
            ctx.output.write(f"Total:  {len(CHAT_COMMANDS.keys())}")
        for command, details in CHAT_COMMANDS.items():
            if len(args) > 0:
                if command != args[0]:
                    continue
            ctx.output.write(f"\t{highlight(command, Fore.BLUE)} : {highlight(details["description"], Fore.RED)} ({details["example"]}) {highlight("[DEBUG ONLY]", Fore.CYAN) if details["debug"] else ""}")

    @chat_command("cat", description="Reads the contents of a file.", example="cat file.txt")
    def cat(ctx):
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
    def ls(ctx):
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
    def echo(ctx):
        args=ctx.args
        fixed = " ".join(args)
        ctx.output.write(fixed)
        

    @chat_command("wait", description="Waits for n seconds.", example="wait 10", required_args=1)
    def wait(ctx):
        args=ctx.args
        time.sleep(float(args[0]))

    @chat_command("cd", description="Changes directory.", example="cd ..", required_args=1)
    def cd(ctx):
        args=ctx.args
        path = expand_path(args[0])
        if not os.path.exists(path):
            error(f"{path} does not exist!")
            return
        change_path(path)

    @chat_command("grep", description="Search for a pattern in input or files.", example="grep pattern file.txt", required_args=1)
    def grep(ctx):
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
    def close(ctx):
        sys.exit(1)