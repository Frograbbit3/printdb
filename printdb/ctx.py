from typing import Any
import os
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