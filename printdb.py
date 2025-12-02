import printdb, printdb.api, shlex,os

IS_RUNNING = True
IS_TYPING = False

printdb.load_plugins()
printdb.api.init()
while IS_RUNNING:
    try:
        IS_TYPING = True
        command = input(f"({os.getcwd()})>")
        IS_TYPING = False
        args = shlex.split(command)

        if len(args) > 0:
            printdb.api.send_chat_command(command)

    except KeyboardInterrupt:
        if IS_TYPING:
            break
        else:
            continue