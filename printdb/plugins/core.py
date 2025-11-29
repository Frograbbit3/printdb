from printdb.api import *


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
        for c, fi in enumerate(os.listdir(os.getcwd())):
            if os.path.isdir(fi):
                log(f"\t{fi} {" " * (80-len(fi)-4)}[folder]")
        for fi in os.listdir(os.getcwd()):
            if os.path.isfile(fi):
                log(f"\t{fi}{" " * (80-len(fi)-4)}[file]")

    @chat_command("echo", description="Echos text into output.", example="echo hello, world!")
    def echo(args):
        fixed = " ".join(args)
        log(fixed)
        

    @chat_command("wait", description="Waits for n seconds.", example="wait 10", required_args=1)
    def wait(args):
        time.sleep(float(args[0]))
