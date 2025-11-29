import printdb.api
import importlib
import pkgutil
from printdb import plugins

def load_plugins():
    c=0
    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        importlib.import_module(f"printdb.plugins.{module_name}")
        c=c+1
    printdb.api.log(f"Loaded {c} plugins successfully")