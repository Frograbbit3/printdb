from printdb.api import *
from pathlib import *

class Plugin():
    @chat_command("help", description="Gets command info",example="help {{command}}")
    def help(args):
        if len(args) < 1:
            log("[ALL COMMANDS]")
            log(f"Total:  {len(CHAT_COMMANDS.keys())}")
            for command, details in CHAT_COMMANDS.items():
                log(f"\t{command} : {details["description"]}. ( {details["example"]} )")
        else:
            for command, details in CHAT_COMMANDS.items():
                if command == args[0].lower():
                    log(f"{command} : {details["description"]}. ( {details["example"]} )")
                    break

    @chat_command("cat", description="Reads the contents of a file.", example="cat file.txt", required_args=1)
    def cat(args):
        fi = os.path.join(os.getcwd(), args[0])
        if os.path.exists(fi):
            with open(fi, "r") as file:
                c=file.read()
                if len(c) < 500:
                    log(c)
                else:
                    log(f"{c[0:500]}... ({len(c) - 500} characters remaining)")
        else:
            error("File", fi, "does not exist.")

    @chat_command("ls", description="Gets the files in the current directory", example="ls")
    def ls(args):
        if len(args) > 0:
            PATH = expand_path(args[0])
        else:
            PATH=CURRENT_PATH
        _FILES = os.listdir(PATH)
        for c, fi in enumerate(_FILES):
            if os.path.isdir(fi):
                if fi.startswith(".") and not "-f" in args:
                    continue
                
                log(f"\t{fi} {" " * (80-len(fi)-4)}[folder]")
        for fi in _FILES:
            if os.path.isfile(fi):
                if fi.startswith(".") and not "-f" in args:
                    continue
                log(f"\t{fi}{" " * (80-len(fi)-4)} [file]")

    @chat_command("echo", description="Echos text into output.", example="echo hello, world!")
    def echo(args):
        fixed = " ".join(args)
        log(fixed)
        

    @chat_command("wait", description="Waits for n seconds.", example="wait 10", required_args=1)
    def wait(args):
        time.sleep(float(args[0]))

    @chat_command("cd", description="Changes directory.", example="cd ..", required_args=1)
    def cd(args):
        path = expand_path(args[0])
        if not os.path.exists(path):
            error(f"{path} does not exist!")
            return
        change_path(path)