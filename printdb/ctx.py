from typing import Any
import os,readline,printdb
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

        # If redirecting, write to file
        if self._file:
            self._file.write(text)
            self._file.flush()
            return

        # Otherwise write to terminal
        print(text, end="", flush=self.flush_enabled)
        self.logs.append(text)

    def read(self):
        return "".join(self.logs)

class CommandContext:
    def __init__(self, args:list[str]):
        self.args = args
        self.input = StreamingLogs()
        self.output = StreamingLogs()
        self.env = os.getcwd()
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