import re, os, shutil, platform, subprocess, json5, shlex, pathlib,printdb.api

ALIAS_NAME = re.compile(r'^[A-Za-z0-9_-]+$')

def validate_alias(alias: str) -> bool:
    if ALIAS_NAME.match(alias):
        return True
    return False


def path_exists(*args):
    return os.path.exists(os.path.join(*list(args)))

def path_join(*args):
    return os.path.join(*list(args))

def create_folder(path: str) -> None:
    if not path_exists(path):
        os.mkdir(path)

def copy_file(file1: str, file2: str) -> None:
    if path_exists(file1):
        shutil.copyfile(file1,file2)

def open_file(file1: str) -> None:
    if path_exists(file1):
        if platform.system() == "Windows":
            os.startfile(file1)  # Windows built-in
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file1])
        else:  # Linux
            subprocess.run(["xdg-open", file1])

def tokenize_args(s: str) -> tuple[str, list[str]]:
    # work on command stuff
    MACRO_BLOCK_REGEX = re.compile(r'\$\{([^}]*)\}')
    matches = MACRO_BLOCK_REGEX.findall(s)
    for cmd in matches:
        #recursively parse the ${command}
        output = printdb.api.send_chat_command(cmd, silent=True) 
        s = s.replace(f"${{{cmd}}}", f'"{output}"')


    tokens = []
    current = []
    depth = 0
    in_single = False
    in_double = False

    for c in s:

        if c == "'" and not in_double:
            in_single = not in_single
            current.append(c)
            continue


        if c == '"' and not in_single:
            in_double = not in_double
            current.append(c)
            continue


        if not in_single and not in_double:
            if c in "{[":
                depth += 1
            elif c in "}]":
                depth -= 1


        if c.isspace() and depth == 0 and not in_single and not in_double:
            if current:
                tokens.append("".join(current))
                current = []
            continue

        current.append(c)

    if current:
        tokens.append("".join(current))

    if not tokens:
        return ("", [])

    return tokens[0], tokens[1:]


def is_path(s: str) -> bool:
    if os.path.exists(printdb.api.expand_path(s)):
        return True
    return False



def convert_str(s: str):
    nones = ["none", "null", "NaN"]
    allowed_trues = ["true", "yes"]
    allowed_falses = ["false", "no"]
    def is_float(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False
    def is_int(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False
    def is_bool(s: str) -> bool:
        if s.lower() in allowed_trues or s.lower() in allowed_falses:
            return True
        return False

    def is_none(s: str) -> bool:
        return s in nones
    
    def is_json(s: str) -> bool:
        try:
            m = json5.loads(s)   
            return True
        except Exception as e:
            return False 
        
    if is_int(s):
        return int(s)
    if is_float(s):
        return float(s)
    if is_bool(s):
        if s.lower() in allowed_trues:
            return True
        else:
            return False
    if is_none(s):
        return None
    if is_json(s):
        return json5.loads(s)
    if is_path(s):
        return pathlib.Path(printdb.api.expand_path(s))
    
    
    return s

def pretty(s):
    if isinstance(s, type):
        return s.__name__