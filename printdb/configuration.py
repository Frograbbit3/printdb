import os, json
from pathlib import Path
def getSavePath() -> str:
    return os.path.join(os.path.expanduser("~"),"printdb")