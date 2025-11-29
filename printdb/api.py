import random,time,json,os,shlex,threading,linecache
from typing import Any
import readline
from colorama import Fore, Style, init

CHAT_COMMANDS: dict[str, Any] = {}
IS_RUNNING = True
USE_ANSI_ESCAPE = True
PREVIOUS_LOGS: str = []
USE_DEBUG_MODE = True # allows debug-only commands to exist

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

def trace_error(plugin,er):
    tb = er.__traceback__
    while tb.tb_next:
        tb = tb.tb_next
    filename = tb.tb_frame.f_code.co_filename
    lineno = tb.tb_lineno
    linecache.checkcache(filename) #fuck you.
    code = linecache.getline(filename, lineno).strip()
    ty = type(er).__name__
    error(f"{ty} raised in {plugin["function"].__module__}.{plugin["function"].__name__} @ Line {lineno}\n\tFile {filename}\n\t{code} <--- [HERE]\n{er}")

def chat_command(command: str, description="",example="", required_args=0):   
    global CHAT_COMMANDS   
    def decorator(func):
        global CHAT_COMMANDS
        if func not in CHAT_COMMANDS.items():
            CHAT_COMMANDS[command] = {"function":func,"description":description, "example":example, "required_args":int(required_args),"module":func.__module__}
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator

def call_chat_command(command: str, args):
    global CHAT_COMMANDS
    for cmd,v in CHAT_COMMANDS.items():
        if cmd != command:
            continue
        if (len(args) < int(v["required_args"])):
            error("Not enough args for command", command+".", "Wants:",v["required_args"], "Provided:",len(args))
            return
        else:
            try:
                v["function"](args)
            except Exception as e:
                trace_error(v, e)
            return
    error("Command", command, "not found!")
    return
