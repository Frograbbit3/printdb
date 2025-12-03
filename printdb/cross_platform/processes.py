import os, subprocess, threading
from printdb.ctx import StreamingLogs

class Process:
    def __init__(self, path: str, args: list[str]):
        self._subproc_args = [path]
        self._subproc_args.extend(args)
        self._path = path
        self._thr = threading.Thread(target=self._thread, daemon=True)
        self.output = StreamingLogs()
        self.input = StreamingLogs()
        self.error = StreamingLogs()
        self.complete = False
        self.return_code = 0
    def run(self):
        self._process = subprocess.Popen(
            self._subproc_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        self._thr.start()
    def block(self):
        if self._process is not None:
            self._process.wait()
        self.terminate()
    def _thread(self):
        while not self.complete:
            if self._process is not None:
                for line in self._process.stdout:
                    self.output.write(line)
                if self._process.returncode is not None:
                    self.return_code = self._process.returncode
                    self.terminate()
    def terminate(self):
        if self._process is not None:
            self._process.terminate()
            self.complete = True
            self.return_code = self._process.returncode
            if threading.current_thread() is not self._thr:
                self._thr.join()