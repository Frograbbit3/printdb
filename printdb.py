import printdb, printdb.api, shlex,os

IS_RUNNING = True

printdb.load_plugins()
printdb.api.init()
while IS_RUNNING:
    try:
        command = input(f"({os.getcwd()})>")
        if "|" in command:
            parts = [p.strip() for p in command.split("|")]
            last_output = None

            for i,p in enumerate(parts):
            
                
                # Call command with last_output as stdin
                last_output = printdb.api.call_chat_command(
                    command,
                    input=last_output,   # <--- THIS is the only thing you need
                    pipe_output=None,
                    append=False,
                    pipe_chain=not (i == len(parts)-1)
                )

            # after pipeline, last_output is the final result
            continue

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
                command,
                pipe_output=FILENAME,    # <-- EXACT behavior you want
                append=APPEND
            )

    except KeyboardInterrupt:
        pass