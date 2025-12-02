from typing import Any
import os,readline
class StreamingLogs:
    def __init__(self):
        self.logs: list[str] = []
    def write(self, content: Any, end="\n"):
        self.logs.append(str(content)+end)
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