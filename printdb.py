import printdb, printdb.api, shlex,os

IS_RUNNING = True

printdb.load_plugins()
printdb.api.init()
while IS_RUNNING:
    try:
        command = input(f"({os.getcwd()})>")

        APPEND = False
        FILENAME = None

        # Detect >> (append)
        if ">>" in command:
            parts = command.split(">>", 1)
            command = parts[0].strip()
            FILENAME = parts[1].strip()
            APPEND = True

        # Detect > (write), but only if >> wasn't used
        elif ">" in command:
            parts = command.split(">", 1)
            command = parts[0].strip()
            FILENAME = parts[1].strip()

        args = shlex.split(command)

        if len(args) > 0:
            printdb.api.call_chat_command(
                args[0],
                args[1:],
                pipe_output=FILENAME,    # <-- EXACT behavior you want
                append=APPEND
            )

    except KeyboardInterrupt:
        IS_RUNNING=False