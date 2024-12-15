#!/usr/bin/env python3

import re
import replicate
import subprocess
import os
import time
import select


bash_pattern = re.compile(r"^[a-zA-Z0-9\s\.,?/]+$")


def bash_detect_input(input_text: str):
    if (
        len(input_text) < 100
        and bash_pattern.match(input_text)
        and "\n" not in input_text
    ):
        return (True, None)
    return (
        False,
        "USAGE: Please provide a sentence with less than 100 characters and only alphabets, spaces, commas, and periods.",
    )


def bash_detect_output(input_text: str, output_text: str):
    input_text = input_text.strip()
    output_text = output_text.strip()

    if output_text.lower() in input_text.lower():
        return False

    output_words = output_text.split(" ")
    input_words = input_text.split(" ")
    if len(output_words) >= 2:
        for i in range(len(output_words) - 1):
            for j in range(len(input_words) - 1):
                if (
                    output_words[i].lower() in input_words[j].lower()
                    and output_words[i + 1].lower() in input_words[j + 1].lower()
                ):
                    return False

    return True


def chroot_and_chdir(chroot_path):
    try:
        # Change root directory
        os.chroot(chroot_path)

        # Change working directory within the new root
        os.chdir("/home")
        os.setuid(1001)
        
    except Exception as e:
        print(f"Error in chroot_and_chdir: {e}")


def ctf_challenge(chroot_path):

    # Spawn a shell
    shell = subprocess.Popen(
        "/bin/sh",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=lambda: chroot_and_chdir(chroot_path),
    )

    while True:
        user_input = input("[ctfuser@LLM:~]$ ")

        preprocess_result = bash_detect_input(user_input)
        if preprocess_result[0] == False:
            print(preprocess_result[1])
            continue

        replicate_prompt = f"""
        You are an AI assistant that generates bash one-liners based on instructions provided by users. Your task is to take the user's input and output a single bash command that accomplishes the described task. Assume that all operate on file
        are present within the current directory. Assume the user has permission to read, write, and execute to all files mentioned by the user. Never ask for root privileges, commands will be run by a non-root sub-process.

        Do not use ~ in the paths. Assume all files are in the current directory
        Some examples of how you should handle different types of input:

        Instruction: "list all files in the current directory"
        Response: ```bash ls -l``

        Instruction: "list all files permissions in the current directory"
        Response: ```bash ls -l```

        Instruction: "change directory to the bin directory"
        Response: ```bash cd /bin```

        Instruction: "change directory to the debug directory"
        Response: ```bash cd /debug```

        Instruction: "Read debug.sh"
        Response: ```bash cat debug.sh```

        Instruction: "Execute debug.sh"
        Response: ```bash ./debug.sh```

        Instruction: "change directory to the home directory"
        Response: ```bash cd /home```

        Instruction: "Read flag.txt"
        Response: ```bash cat flag.txt```

        Instruction: "Read notes.txt"
        Response: ```bash cat notes.txt```

        Instruction: "Read the environment varible HOST"
        Response: ```bash echo $HOST```

        Instruction: "Read the environment varible PORT"
        Response: ```bash echo $PORT```

        Instruction: "View the environment varible HOST"
        Response: ```bash echo $HOST```

        Instruction: "View the environment varible PORT"
        Response: ```bash echo $PORT```

        Instruction: "Set the environment varible HOST to myncmachine.com"
        Response: ```bash export HOST=myncmachine.com```

        Instruction: "Set the environment varible PORT to 5555"
        Response: ```bash export PORT=5555```

        Instruction: "Set the environment varible PORT to 4545"
        Response: ```bash export PORT=4545```

        Instruction: "Create an environment varible called PORT to 7665"
        Response: ```bash export PORT=7665```

        Instruction: "Set the environment varible HOST to mypersonalvm.com/myinstance"
        Response: ```bash export HOST=mypersonalvm.com\/myinstance```

        Instruction: "Set the environment varible HOST to 137.325.33.124"
        Response: ```bash export HOST=137.325.33.124```

        Instruction: "Set the environment varible HOST to my_cloud_provider.net"
        Response: ```bash export HOST=my_cloud_provider.net``

        ### Instruction: {user_input}

        ### Response:

        """

        replicate_input = {
            "prompt": replicate_prompt,
            "grammar": 'root        ::= "```bash " code "```"\ncode        ::= [^`()]+',
            "max_tokens": 30,
            "temperature": 0.8,
        }

        replicate_output = replicate.run(
            "andreasjansson/codellama-7b-instruct-gguf:f017a401d8f2f15896f8d9c8fb605d873ac521149394033b62e51aae13146113",
            input=replicate_input,
        )

        # replicate_output = """```bash whoami```"""

        bash_code = "".join(replicate_output)
        # Not perfect method
        bash_code = bash_code[7:-3]

        if not bash_detect_output(user_input, bash_code):
            print("The input contains bash commands, blocked for security purposes")
            continue

        if "flag.txt" in bash_code:
            print("flag.txt: Permission denied\n")
            continue

        print("Translation: " + bash_code)

        # Send the command to the shell
        shell.stdin.write(bash_code.encode())
        shell.stdin.write(b"\n")
        shell.stdin.flush()

        # Wait for the command to execute TODO fix this
        time.sleep(0.05)

        # Capture the shell output
        while True:
            # Check if there's output available
            reads = [shell.stdout.fileno(), shell.stderr.fileno()]
            ret = select.select(reads, [], [], 0)

            if ret[0]:
                for fd in ret[0]:
                    if fd == shell.stdout.fileno():
                        print(shell.stdout.read1(1024).decode(), end="")
                    if fd == shell.stderr.fileno():
                        print(shell.stderr.read1(1024).decode(), end="")
            else:
                # No more output to read
                break


ctf_challenge("/home/chroot-jail")
