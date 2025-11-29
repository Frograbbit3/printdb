import random,time,json,os,shlex,threading
from typing import Any
import readline
from colorama import Fore, Style, init

CHAT_COMMANDS: dict[str, Any] = {}
IS_RUNNING = True
USE_ANSI_ESCAPE = True
PREVIOUS_LOGS: str = []

def fix_args(args)->list[str]:
    global PREVIOUS_LOGS
    new_args = []
    for arg in args:
        new_args.append(str(arg))
    return new_args

def log(*args) -> None:
    global PREVIOUS_LOGS
    PREVIOUS_LOGS.append(" ".join(fix_args(args)))
    print(" ".join(fix_args(args)))


def error(*args) -> None:
    PREVIOUS_LOGS.append(" ".join(fix_args(args)))
    if USE_ANSI_ESCAPE:
        print(Fore.RED +"[ERROR]:", " ".join(fix_args(args)) + Fore.RESET)
    else:
        print("".join(fix_args(args)))


def chat_command(command: str, description="",example="", required_args=0):      
    def decorator(func):
        if func not in CHAT_COMMANDS.items():
            CHAT_COMMANDS[command] = {"function":func,"description":description, "example":example, "required_args":int(required_args)}
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator

def call_chat_command(command: str, args, use_history=False):
    global CHAT_COMMANDS,PREVIOUS_LOGS
    if not use_history:
        PREVIOUS_LOGS = []
    else:
        args=["".join(PREVIOUS_LOGS)]
    print(args)
    for cmd,v in CHAT_COMMANDS.items():
        if cmd != command:
            continue
        if (len(args) < int(v["required_args"])):
            error("Not enough args for command", command+".", "Wants:",v["required_args"], "Provided:",len(args))
            return
        else:
            v["function"](args)
            return
    error("Command", command, "not found!")
    return

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

init()
while IS_RUNNING:
    try:
        command = input(f"({os.getcwd()})>")
        piped = command.split(">>")
        prev = ""
        for i,cmd in enumerate(piped):
            args =  shlex.split(cmd)
            if len(args) > 0:
                try:
                    call_chat_command(args[0], args[1::],not (i == 0))
                except KeyboardInterrupt:
                    break
    except KeyboardInterrupt:
        IS_RUNNING=False