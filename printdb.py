import printdb, printdb.api, shlex,os

IS_RUNNING = True

printdb.load_plugins()
printdb.api.init()
while IS_RUNNING:
    try:
        command = input(f"({os.getcwd()})>")
        args = shlex.split(command)
        if len(args) > 0:
            printdb.api.call_chat_command(args[0], args[1::])
    except KeyboardInterrupt:
        IS_RUNNING=False