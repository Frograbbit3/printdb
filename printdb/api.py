import random,time,json,os,shlex,threading,linecache,time
from typing import Any
import readline
from colorama import Fore, Style
import colorama
import printdb.ctx
import printdb.configuration
import printdb.plugin_manager
import printdb.utils as utils
import shutil,subprocess,re

CHAT_COMMANDS: dict[str, Any] = {}
IS_RUNNING = True
USE_ANSI_ESCAPE = True
PREVIOUS_LOGS: list[str] = []
USE_DEBUG_MODE = True # allows debug-only commands to exist
CURRENT_PATH: str = os.getcwd()
ALIASES: dict[str,str] = {}
CONFIGURATION = None
SANDBOXED_MODE = True
RAW_COMMANDS: list[str] = []
START_TIME: int = 0

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

import os


def init():
    global START_TIME
    colorama.init()
    load_configuration()
    START_TIME = time.time()
def load_configuration():
    global CONFIGURATION,ALIASES,USE_DEBUG_MODE,SANDBOXED_MODE
    CONFIGURATION = printdb.configuration.Configuration()
    CONFIGURATION.load_save()
    if getattr(CONFIGURATION, "command_history", None) is not None:
        for cmd in CONFIGURATION.command_history:
            readline.add_history(cmd)
    else:
        CONFIGURATION.command_history = []
    if getattr(CONFIGURATION, "last_path", None) is not None:
        change_path(CONFIGURATION.last_path)
    else:
        CONFIGURATION.last_path = os.path.expanduser("~")
    if CONFIGURATION.aliases is None:
        CONFIGURATION.aliases = {}
    else:
        ALIASES = CONFIGURATION.aliases
    if CONFIGURATION.debug is None:
        CONFIGURATION.debug = USE_DEBUG_MODE
    else:
        USE_DEBUG_MODE = CONFIGURATION.debug
    if CONFIGURATION.sandboxed is None:
        CONFIGURATION.sandboxed=SANDBOXED_MODE
    else:
        SANDBOXED_MODE=CONFIGURATION.sandboxed
    
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")



def get_plugin_stats(plugin):
    if plugin is None:
        return {
            "name": "[UNKNOWN]",
            "version": "[UNKNOWN]",
            "author": "[UNKNOWN]"
        }
    if getattr(plugin, "META", False):
        return {
            "name": plugin.META.name,
            "author": plugin.META.author,
            "version": plugin.META.version,
            "description": plugin.META.description,
            "id": plugin.META.id
        }
    if not getattr(plugin, "PLUGIN_NAME", False):
        return {
            "name": "[UNKNOWN]",
            "version": "[UNKNOWN]",
            "author": "[UNKNOWN]"
        }
    return {
        "name": plugin.PLUGIN_NAME,
        "version": plugin.PLUGIN_VERSION,
        "author": plugin.PLUGIN_AUTHOR
    }

def get_plugin_from_command(func):
    for p in printdb.plugin_manager.get_plugins():
        if p.__module__ == func["module"]:    
            return p
    return None    

def save_configuration():
    global CONFIGURATION
    CONFIGURATION.save_save()

def get_git_branch(directory: str):
    directory = os.path.abspath(directory)
    while True:
        git_dir = os.path.join(directory, ".git")
        head_file = os.path.join(git_dir, "HEAD")

        if os.path.isfile(head_file):
            with open(head_file, "r") as f:
                content = f.read().strip()
            if content.startswith("ref:"):
                return content.split("/")[-1]
            return None
        
        parent = os.path.dirname(directory)
        if parent == directory:
            return None

        directory = parent


def register_alias(command:str,alias:str) -> None:
    global ALIASES,CONFIGURATION
    ALIASES[alias] = command
    CONFIGURATION.aliases = ALIASES.copy()

def completer(text, state):
    global RAW_COMMANDS
    commands = RAW_COMMANDS
        
    matches = [cmd for cmd in commands if cmd.startswith(text)]
        
    try:
        return matches[state]
    except IndexError:
        return None


def expand_path(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))

def change_path(new_path: str) -> None:
    global CURRENT_PATH
    if not os.path.exists(new_path):
        raise Exception(f"Could not change to path {new_path}: Path does not exist.")
    os.chdir(new_path)
    CURRENT_PATH = os.getcwd()
    CONFIGURATION.last_path = CURRENT_PATH

def input_prompt()->str:
    path = os.getcwd()
    st = f"{highlight(f"({path})", Fore.GREEN)} "
    gt = get_git_branch(os.getcwd())
    if gt is not None:
        st += f"{highlight("@ "+gt.strip(), Fore.BLUE)}"
    return st + " >"

def highlight(text: str, color=Fore.RED):
    if not USE_ANSI_ESCAPE:
        return text
    return color+str(text)+Style.RESET_ALL

def trace_error(plugin,er):
    tb = er.__traceback__
    while tb.tb_next:
        tb = tb.tb_next
    filename = tb.tb_frame.f_code.co_filename
    lineno = tb.tb_lineno
    linecache.checkcache(filename) #fuck you.
    code = linecache.getline(filename, lineno).strip()
    ty = type(er).__name__
    return f"{ty} raised in {plugin["function"].__module__}.{plugin["function"].__name__} @ Line {lineno}\n\tFile {filename}\n\t{code} <--- [HERE]\n{er}"

def chat_command(command: str, description="",example="", required_args=0, is_debug=False, is_hidden=False, is_sandboxed=False):   
    global CHAT_COMMANDS, RAW_COMMANDS
    if not USE_DEBUG_MODE and is_debug:
        def ghost_decor(*args, **kwargs):
            pass
        return ghost_decor
    def decorator(func):
        global CHAT_COMMANDS
        if func not in CHAT_COMMANDS.items():
            CHAT_COMMANDS[command] = {"hidden":is_hidden, "sandboxed": is_sandboxed, "function":func,"description":description, "example":example, "required_args":int(required_args),"module":func.__module__,"debug":is_debug}
            RAW_COMMANDS.append(command)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator

def split_args(command: str) -> list[str]:
    split =shlex.split(command)
    return split[0], split[1::]

def split_pipes(command: str) -> list[str]:
    if "|" in command:
        parts = [p.strip() for p in command.split("|")]
        return parts
    else:
        return [command]

def split_file_names(full_command: str):
    if ">>" in full_command:
        MODE="append"
        file = full_command.split(">>")[1]
        cmd = full_command.split(">>")[0]
        return (cmd.lstrip().rstrip(), file.lstrip().rstrip(), MODE)
    elif ">" in full_command:
        MODE="write"
        file = full_command.split(">")[1]
        cmd = full_command.split(">")[0]
        return (cmd.lstrip().rstrip(), file.lstrip().rstrip(), MODE)
    else:
        return (full_command, None, None)
    
def send_chat_command(command:str, append=False):
    global CONFIGURATION
    full_command = command
    CONFIGURATION.command_history.append(command)
    command, file_name, mode =split_file_names(command)
    command, args = utils.tokenize_args(command)
    for alias,cmd2 in ALIASES.items():
        if command == alias:
            command, new_args = utils.tokenize_args(cmd2)
            args = new_args + args
            break
    
    pipes = split_pipes(command+" "+" ".join(args))
    if len(pipes) < 2:
        return call_chat_command(command, args=args,output=file_name, append=(mode == "append"),full_command=full_command)
    for i,cmd in enumerate(pipes):
        cd, ags = utils.tokenize_args(cmd)
        if i == 0:
            command_output = call_chat_command(cd,args=ags,mask_input=True,full_command=full_command)
        elif i < len(pipes)-1:
            command_output = call_chat_command(cd,args=ags,input=command_output,mask_input=True,full_command=full_command)
        else:
            command_output = call_chat_command(cd,args=ags,input=command_output,mask_input=False,output=file_name, append=(mode == "append"),full_command=full_command) 
        

def call_chat_command(command: str, args=[], append=False, input=None, mask_input=False, output = None, full_command=None):
    global CHAT_COMMANDS,PREVIOUS_LOGS
    PREVIOUS_LOGS.clear()
    if os.path.exists(os.path.join(os.getcwd(),command)):
        with open(os.path.join(os.getcwd(),command), "r") as m:
            contents=m.read()
            if contents.startswith("#!"):
                interpeter = contents.splitlines()[0][2::]
                if interpeter.startswith("/usr/bin/env"):
                    interpeter = interpeter.replace("/usr/bin/env", "").strip()
                    p = shutil.which(interpeter)
                    if p:
                        try:
                            subprocess.run([p, os.path.join(os.getcwd(),command)])
                        except KeyboardInterrupt:
                            return
                else:
                    try:
                        subprocess.run([interpeter, os.path.join(os.getcwd(),command)])
                    except KeyboardInterrupt:
                         return
                return

    for cmd,v in CHAT_COMMANDS.items():
        if cmd != command:
            continue
        if (len(args) < int(v["required_args"])):
            error("Not enough args for command", command+".", "Wants:",v["required_args"], "Provided:",len(args))
            return
        else:
            try:
                if v["sandboxed"] and SANDBOXED_MODE:
                    error("This command is disabled due to sandbox mode.")
                    return ""
                context = printdb.ctx.CommandContext(args,full_command)
                if input is not None:
                    context.input.write(input,end="")
                plugin = get_plugin_from_command(v)
                if output is not None or mask_input:
                    context.output.flush_enabled = False
                if output is not None :
                    context.output.start_redirect( os.path.join(os.getcwd(), output),"w" if not append else "a")

                try:
                    v["function"](plugin, context)
                except KeyboardInterrupt:
                    pass
                if output is not None and not mask_input:
                    context.output.stop_redirect()

                
            except Exception as e:
                context.output.write(highlight(trace_error(v, e)))
                return None
            return context.output.read()

    error("Command", command, "not found!")
    return None
