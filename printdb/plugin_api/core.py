import getpass, re,shutil, builtins
import printdb.plugin_manager
import printdb.base_plugin as base
import printdb.api,printdb.utils
import inspect

ANSI_COLOR_CODES = {
    "reset": "\033[0m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bold": "\033[1m",
}


def get_username():
    return getpass.getuser()

def get_plugin_by_id(id: str) -> base.BasePlugin:
    for plugin in printdb.plugin_manager.PLUGINS:
        if plugin.META.id == id:
            return plugin
    return None

def get_plugin_ids() -> list[str]:
    plugin_ids: list[str] = []
    for plugin in printdb.plugin_manager.PLUGINS:
        plugin_ids.append(plugin.META.id)
    return plugin_ids

def ansi_format(st: str) -> str:
    for name, color in ANSI_COLOR_CODES.items():
        st = st.replace(f"[[{name}]]", color)
    st+=ANSI_COLOR_CODES["reset"]
    return st

def pad_string(st, tiles, align="center", left_padding=0, right_padding=0):
    content = st
    total = tiles - len(content)

    # Apply manual paddings
    total -= (left_padding + right_padding)

    if total < 0:
        total = 0  # avoid negative spacing

    if align == "left":
        left = left_padding
        right = total + right_padding
    elif align == "right":
        left = total + left_padding
        right = right_padding
    else:  # center
        half = total // 2
        left = half + left_padding
        right = total - half + right_padding

    return (" " * left) + content + (" " * right)

def columnize(items, padding=2):
    # --- embedded ANSI stripper ---
    ANSI = re.compile(r'\x1b\[[0-9;]*m')

    def visible_len(s):
        return len(ANSI.sub("", s))

    if not items:
        return ""

    # --- determine widest item ---
    max_width = max(visible_len(item) for item in items) + padding

    # --- detect terminal width ---
    term_width = shutil.get_terminal_size().columns

    # --- compute how many columns fit ---
    columns = max(1, term_width // max_width)

    # --- build rows ---
    lines = []
    for i in range(0, len(items), columns):
        row = items[i:i + columns]
        line = ""
        for entry in row:
            space = max_width - visible_len(entry)
            line += entry + (" " * space)
        lines.append(line.rstrip())

    return "\n".join(lines)



def get_args(cmd: str):
    # getting the command

    command_func = None
    for command, details in printdb.api.CHAT_COMMANDS.items():
        if command == cmd:
            command_func = details["function"]
            break
    
    if command_func == None:
        return None
    
    sig = inspect.signature(command_func)
    params = list(sig.parameters.values())[2:]  #skipping the first two (self, ctx)
     
    if len(params) < 1:
        return None
    
    args = {}

    for param in params:
    
        args[param.name] = {
            "type": printdb.utils.pretty(param.annotation),
            "optional": (param.empty != inspect._empty),
            "variadic": (param.kind == inspect.Parameter.VAR_POSITIONAL),
            "default": param.default if param.default != inspect._empty else None
        }

    return
