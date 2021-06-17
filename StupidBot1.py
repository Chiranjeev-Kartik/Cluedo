import socket
import threading

host = "127.0.0.1"
# If you are playing in LAN then make sure you chance the host address to IPV4 address of game server.

user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_socket.connect((host, 55555))

nickname = 'StupidBot1'
Mycards = [[], [], []]
suspects = {1: "Colonel Mustard", 2: "Professor Plum", 3: "Reverend Green", 4: "Mrs. Peacock", 5: "Miss Scarlett",
            6: "Mrs. White"}
weapon = {1: "Dagger", 2: "Candlestick", 3: "Revolver", 4: "Rope", 5: "Lead piping", 6: "Spanner"}
rooms = {1: "Hall", 2: "Lounge", 3: "Library", 4: "Kitchen", 5: "Billiard Room", 6: "Study"}


def send_message():
    while True:
        try:
            message = input()
            user_socket.send(message.encode("utf-8"))
        except Exception as error:
            print(f"Send Error:{error}")
            break
    return None


def send_bot_message(bot_message):
    try:
        print(f"trying:{bot_message}")
        message = bot_message
        user_socket.send(message.encode("utf-8"))
    except Exception as error:
        print(f"Send Error:{error}")
    return None


def listening():
    while True:
        try:
            message = user_socket.recv(1024).decode("utf-8")
            if not message:
                break
            else:
                print(message)
                bot_act_on_message(message)
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    return None


def remember_cards(cards_message):
    cards_to_remember = cards_message
    print(f"I need to remember these cards:{cards_to_remember}")
    return None


def bot_act_on_message(message):
    if message.find('nickname') != -1:
        print(f"Sending Nickname")
        send_bot_message(nickname)
    elif message.find('Want to enter in a room') != -1:
        print(f"Saying yes to enter a room")
        send_bot_message("y")
    elif message.find('Your Cards') != -1:
        print(f"Need to remember these cards")
        remember_cards(message)
    elif message.find('Roll Dice') != -1:
        print(f"Trying to roll dice")
        send_bot_message("y")
    else:
        print(f"I need to do something else")
    return None


t1 = threading.Thread(target=listening, daemon=True)
t1.start()
send_message()
