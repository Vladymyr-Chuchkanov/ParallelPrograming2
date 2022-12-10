import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back



init()
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]
_type = "<MODE>"





def nick_enter():
    global name
    name = input("Введіть ваш нік: ")



def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)



client_color = random.choice(colors)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
separator_token = "<SEP>"
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
name = ""

nick_enter()
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send =  input(">")

    if to_send.lower() == 'q':
        break

    if to_send.lower()=="/private":
        name1 = input("Приватні повідомлення по ніку: ")
        name1 = name1.strip()
        to_send = input(">")
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}]{name1}{_type} {name}{separator_token}{to_send}{Fore.RESET}"
        s.send(to_send.encode())
    else:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}]0{_type} {name}{separator_token}{to_send}{Fore.RESET}"
        s.send(to_send.encode())



s.close()

