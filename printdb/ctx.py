from typing import Any, Type
import os,readline,printdb,inspect
from dataclasses import dataclass
class StreamingLogs:
    def __init__(self):
        self.logs: list[str] = []
        self.flush_enabled = True
        self.redirect_file = None
        self.redirect_mode = None
        self._file = None

    def start_redirect(self, path, mode="w"):
        self.redirect_file = path
        self.redirect_mode = mode
        self._file = open(path, mode)

    def stop_redirect(self):
        if self._file:
            self._file.flush()
            self._file.close()
        self._file = None
        self.redirect_file = None
        self.redirect_mode = None

    def write(self, content: Any, end="\n"):
        text = str(content) + end

        if self._file:
            self._file.write(text)
            self._file.flush()
            return

        # Otherwise write to terminal
        if self.flush_enabled:
            print(text,end="")
        self.logs.append(text)

    def read(self):
        return "".join(self.logs)


class CommandContext:
    def __init__(self, args:list[str], full_command:str, refrence_func):
        self.args = args
        self.refunc = refrence_func
        self.typed_args = []
        self._fixargs()
        self.input = StreamingLogs()
        self.output = StreamingLogs()
        self.env = os.getcwd()
        self.full_command = full_command
    def _fixargs(self):
        new_args = []
        for arg in self.args:
            new_args.append(printdb.utils.convert_str(arg))
        self.args = new_args
        sig = inspect.signature(self.refunc)
        if len(sig.parameters.values()) < 3:
            return
        params = list(sig.parameters.values())[2:]  # skip self, ctx

        typed = []
        provided = self.args
        pi = 0 
        ai = 0 

        while pi < len(params):
            p = params[pi]
            name = p.name
            annotation = p.annotation
            default = p.default
            variadic = (p.kind == inspect.Parameter.VAR_POSITIONAL)

            if annotation is inspect._empty:
                annotation = str

            if variadic:
                typed.extend(provided[ai:])
                ai = len(provided)
                break


            if ai >= len(provided):
                if default is not inspect._empty:
                    typed.append(default)
                    pi += 1
                    continue
                raise Exception(f"Missing required argument '{name}'")
            val = provided[ai]

            if not isinstance(val, annotation):
                raise Exception(f"Argument '{name}' expected {printdb.utils.pretty(annotation)}, got {printdb.utils.pretty(type(val))} ({val})")

            typed.append(val)
            ai += 1
            pi += 1
            
        if ai < len(provided):
            raise Exception("Too many arguments provided")

        self.typed_args = typed



            
    def confirm(self, message:str, preferred=True) -> bool:
        option1 = "Y" if preferred else "y"
        option2 = "n" if preferred else "N"
        opt = input(f"{message} ({option1}/{option2})").lower()

        if opt == option1.lower():
            readline.remove_history_item(readline.get_current_history_length()-1)
            return True
        else:
            readline.remove_history_item(readline.get_current_history_length()-1)
            return False