#!/usr/bin/env python3
import printdb, printdb.api, shlex,os
from colorama import Fore
IS_RUNNING = True
IS_TYPING = False

printdb.load_plugins()
printdb.api.init()
while IS_RUNNING:
    try:
        IS_TYPING = True
        command = input(printdb.api.input_prompt())
        IS_TYPING = False
        args = shlex.split(command)

        if len(args) > 0:
            printdb.api.send_chat_command(command)

    except KeyboardInterrupt:
        if IS_TYPING:
            break
        else:
            continue