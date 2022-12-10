
import socket
from threading import Thread


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"
_type = "<MODE>"
LOGS = []
client_names = []
client_sockets = set()

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):

    while True:
        mode = ""
        name = ""
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            LOGS.append(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            mode = msg.split(_type)[0]
            mode = mode.split("]")[1]
            msg = msg.replace(mode+_type,"")
            name = msg.split(separator_token)[0].split("]")[1].strip()
            if (name,cs) not in client_names:
                client_names.append((name,cs))
            msg = msg.replace(separator_token, ": ")


        if mode == "0"or mode == "":
            LOGS.append(msg)
            for client_socket in client_sockets:
                client_socket.send(msg.encode())
        else:
            msg = msg.replace(name,"from "+name+" to "+mode)
            LOGS.append(msg)
            for els in client_names:
                if els[0]==mode:
                    els[1].send(msg.encode())
                    for els2 in client_names:
                        if els2[0]==name:
                            els2[1].send(msg.encode())
                            return
            for els2 in client_names:
                if els2[0] == name:
                    els2[1].send("такого ніку немає!".encode())
                    return

while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    LOGS.append(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)

    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()


for cs in client_sockets:
    cs.close()

s.close()