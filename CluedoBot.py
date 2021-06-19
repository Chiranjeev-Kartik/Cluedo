import socket
import threading

host = "127.0.0.1"
# If you are playing in LAN then make sure you chance the host address to IPV4 address of game server.

user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_socket.connect((host, 55555))


def send_message():
    while True:
        try:
            message = input()
            user_socket.send(message.encode("utf-8"))
        except Exception as error:
            print(f"Send Error:{error}")
            break
    return None


def listening():
    while True:
        try:
            message = user_socket.recv(1024).decode("utf-8")
            if not message:
                break
            else:
                print(message)
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    return None


t1 = threading.Thread(target=listening, daemon=True)
t1.start()
send_message()
