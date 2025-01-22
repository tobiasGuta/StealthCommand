# StealthCommand
This script creates a simple TCP server that enables remote command execution. Clients can connect to the server, send commands, and receive the output. Running as a daemon in the background, it operates discreetly and can handle multiple client connections at once. This makes it suitable for tasks like remote administration, and pentesting as it runs silently without user interaction, hiding its output. It also forks the process to ensure it stays active even if the user closes the terminal. The use of threads allows the server to handle multiple clients concurrently, improving scalability, by leveraging the setproctitle module, the script can rename the process, making it harder to detect in system process lists.


https://github.com/user-attachments/assets/1212329f-0b11-46d4-9a93-3382f3f83816

## Installation

```bash
https://github.com/tobiasGuta/StealthCommand.git
```

```bash
cd SteatlhCommand.git
```

Just a heads-up: You'll need to transfer this file to the computer you want to control and install the "setproctitle" module to rename the process.

Note: Feel free to choose any name for the process.

```bash
./stealthcommand.py
```
