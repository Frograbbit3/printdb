import printdb, printdb.api, shlex,os

IS_RUNNING = True

printdb.load_plugins()
printdb.api.init()
while IS_RUNNING:
    try:
        command = input(f"({os.getcwd()})>")
        piped = command.split(">>")
        prev = ""
        for i,cmd in enumerate(piped):
            args =  shlex.split(cmd)
            if len(args) > 0:
                try:
                    printdb.api.call_chat_command(args[0], args[1::],not (i == 0))
                except KeyboardInterrupt:
                    break
    except KeyboardInterrupt:
        IS_RUNNING=False