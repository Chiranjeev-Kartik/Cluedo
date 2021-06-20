import re
import socket
import threading
import random
import time

initialised = False
pattern_1 = r'([A-Za-z0-9-_]*) has ([A-Za-z .]*).'
winning = False


class CluedoBot:
    def __init__(self, ip):
        self.host = ip
        # Various nicknames for Bot.
        self.nickname = iter(['Champ-01', 'RoboCop', 'Bond_Bot', 'Lawliet', 'Conan', 'Chimp'])
        self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_socket.connect((self.host, 55555))
        # Possible Choices
        self.possible_answer = ["Colonel Mustard", "Professor Plum", "Reverend Green", "Mrs. Peacock", "Miss Scarlett",
                                "Mrs. White", "Dagger", "Candlestick", "Revolver", "Rope", "Lead piping", "Spanner",
                                "Hall",
                                "Lounge", "Library", "Kitchen", "Billiard Room", "Study"]
        self.rooms = {1: "Hall", 2: "Lounge", 3: "Library", 4: "Kitchen", 5: "Billiard Room", 6: "Study"}
        self.suspects = {1: "Colonel Mustard", 2: "Professor Plum", 3: "Reverend Green", 4: "Mrs. Peacock",
                         5: "Miss Scarlett",
                         6: "Mrs. White"}
        self.weapon = {1: "Dagger", 2: "Candlestick", 3: "Revolver", 4: "Rope", 5: "Lead piping", 6: "Spanner"}
        t1 = threading.Thread(target=self.listening)
        t1.start()

    def initialise_cards(self, message):
        """
        Eliminates Bot's cards from possible choices.
        """
        global initialised

        if not initialised:
            for i in message.split("'"):
                if i in self.possible_answer:
                    self.possible_answer.remove(i)
        initialised = True
        return None

    def choose_room(self):
        """
        Chooses a room from possible choices
        """
        for key in self.rooms:
            if self.rooms[key] in self.possible_answer:
                self.send_bot_message(str(key))
                break
        return None

    def choose_suspect_and_weapon(self):
        """
        Chooses suspect and weapon from possible choices.
        """
        guess = ''
        for a in self.suspects:
            if self.suspects[a] in self.possible_answer:
                guess = str(a) + " "
                break
        for a in self.weapon:
            if self.weapon[a] in self.possible_answer:
                guess = guess + str(a)
                break
        self.send_bot_message(guess)
        return None

    def send_bot_message(self, bot_message):
        try:
            print(bot_message)
            self.user_socket.send(bot_message.encode("utf-8"))
        except Exception as error:
            print(f"Send Error:{error}")
        return None

    def bot_act_on_message(self, message):
        """
        Match incoming messages from game and react accordingly.
        """
        global winning
        # print(self.possible_answer)
        if 'Hey there' in message:
            time.sleep(1)
            self.send_bot_message(next(self.nickname))
        elif 'This name is not available' in message:
            time.sleep(1)
            self.send_bot_message(next(self.nickname))
        elif 'Your Cards' in message and not initialised:
            self.initialise_cards(message)
        elif "Roll Dice" in message:
            time.sleep(1)
            self.send_bot_message("y")
        elif 'Want to enter in a room' in message:
            time.sleep(1)
            choice = random.choices(['y', 'n'], weights=(98, 2))
            self.send_bot_message(*choice)
        elif 'Choose a room to enter' in message:
            time.sleep(1)
            self.choose_room()
        elif '6.) Mrs. White' in message:
            time.sleep(1)
            self.choose_suspect_and_weapon()
        elif 'Do you want to revel cards' in message:
            time.sleep(1)
            if winning:
                choice = random.choices(['y', 'n'], weights=(98, 2))
            else:
                choice = random.choices(['y', 'n'], weights=(2, 98))
            self.send_bot_message(*choice)
        elif re.fullmatch(pattern_1, message):
            self.possible_answer.remove(re.fullmatch(pattern_1, message).group(2))
        elif 'No proof against' in message:
            time.sleep(1)
            winning = True

    def listening(self):
        while True:
            try:
                message = self.user_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                else:
                    print(message)
                    self.bot_act_on_message(message)
            except Exception as e:
                print(f"Error occurred: {e}")
                break
        return None


if __name__ == '__main__':
    ip_address = '127.0.0.1'
    print("Deploying Bot")
    CluedoBot(ip_address)
