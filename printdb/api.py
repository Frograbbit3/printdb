import random,time,json,os,shlex,threading,linecache
from typing import Any
import readline
from colorama import Fore, Style, init
import printdb.ctx

CHAT_COMMANDS: dict[str, Any] = {}
IS_RUNNING = True
USE_ANSI_ESCAPE = True
PREVIOUS_LOGS: list[str] = []
USE_DEBUG_MODE = True # allows debug-only commands to exist
CURRENT_PATH: str = os.getcwd()

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

def expand_path(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))

def change_path(new_path: str) -> None:
    global CURRENT_PATH
    if not os.path.exists(new_path):
        raise Exception(f"Could not change to path {new_path}: Path does not exist.")
    os.chdir(new_path)
    CURRENT_PATH = os.getcwd()

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

def chat_command(command: str, description="",example="", required_args=0, is_debug=False):   
    global CHAT_COMMANDS
    if not USE_DEBUG_MODE and is_debug:
        def ghost_decor(*args, **kwargs):
            pass
        return ghost_decor
    def decorator(func):
        global CHAT_COMMANDS
        if func not in CHAT_COMMANDS.items():
            CHAT_COMMANDS[command] = {"function":func,"description":description, "example":example, "required_args":int(required_args),"module":func.__module__}
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator

def call_chat_command(command: str, args, pipe_output=None, append=False):
    global CHAT_COMMANDS,PREVIOUS_LOGS
    PREVIOUS_LOGS.clear()
    for cmd,v in CHAT_COMMANDS.items():
        if cmd != command:
            continue
        if (len(args) < int(v["required_args"])):
            error("Not enough args for command", command+".", "Wants:",v["required_args"], "Provided:",len(args))
            return
        else:
            try:
                context = printdb.ctx.CommandContext(args)
                v["function"](context)
                if pipe_output: # append
                    p=os.path.join(os.getcwd(), pipe_output)
                    if append:
                        with open(p, "a") as f:
                            f.write(context.output.read())
                    else:
                        with open(p, "w") as f:
                            f.write(context.output.read())
                else:
                    log(context.output.read())
            except Exception as e:
                trace_error(v, e)
            return
    error("Command", command, "not found!")
    return
