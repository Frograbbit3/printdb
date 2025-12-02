import re

ALIAS_NAME = re.compile(r'^[A-Za-z0-9_-]+$')

def validate_alias(alias: str) -> bool:
    if ALIAS_NAME.match(alias):
        return True
    return False
