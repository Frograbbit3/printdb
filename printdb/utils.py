import re, os, shutil

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
        