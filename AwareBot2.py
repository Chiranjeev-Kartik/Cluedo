import socket
import threading


class Cluedobot:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_socket.connect((self.host, 55555))
        self.suspects = {1: "Colonel Mustard", 2: "Professor Plum", 3: "Reverend Green", 4: "Mrs. Peacock",
                         5: "Miss Scarlett",
                         6: "Mrs. White"}
        self.weapon = {1: "Dagger", 2: "Candlestick", 3: "Revolver", 4: "Rope", 5: "Lead piping", 6: "Spanner"}
        self.rooms = {1: "Hall", 2: "Lounge", 3: "Library", 4: "Kitchen", 5: "Billiard Room", 6: "Study"}

        self.nickname = 'AwareBot2'
        self.remembered_cards = False
        self.possibleAnswer = ["Colonel Mustard", "Professor Plum", "Reverend Green", "Mrs. Peacock", "Miss Scarlett",
                               "Mrs. White", "Dagger", "Candlestick", "Revolver", "Rope", "Lead piping", "Spanner",
                               "Hall",
                               "Lounge", "Library", "Kitchen", "Billiard Room", "Study"]
        self.Mycards = []
        t2 = threading.Thread(target=self.listening, daemon=True)
        t2.start()
        self.listening()

    def send_message(self):
        while True:
            try:
                message = input()
                self.user_socket.send(message.encode("utf-8"))
            except Exception as error:
                print(f"Send Error:{error}")
                break
        return None

    def send_bot_message(self, bot_message):
        try:
            message = bot_message
            print("THIS" + message + "That")
            self.user_socket.send(message.encode("utf-8"))
        except Exception as error:
            print(f"Send Error:{error}")
        return None

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

    def useShownCard(self, lastMessage):
        info = lastMessage[(lastMessage.find("has")+4):lastMessage.find(".Do")]
        self.possibleAnswer.remove(info)
        self.send_bot_message("n")
        return None

    def remember_cards(self, cards_message):
        try1 = cards_message.split("'")
        for x in try1:
            if x in self.possibleAnswer:
                self.possibleAnswer.remove(x)
        self.remembered_cards = True
        self.send_bot_message("y")
        return None

    def chooseRoom(self):
        for a in self.rooms:
            if self.rooms[a] in self.possibleAnswer:
                self.send_bot_message(str(a))
                break
        return None

    def chooseSuspectAndWeapon(self):
        guess = ""
        for a in self.suspects:
            if self.suspects[a] in self.possibleAnswer:
                guess = str(a) + " "
                break
        for a in self.weapon:
            if self.weapon[a] in self.possibleAnswer:
                guess = guess + str(a)
                break
        self.send_bot_message(guess)
        return None

    def bot_act_on_message(self, message):
        if message.find('nickname') != -1:
            print(f"Sending Nickname")
            self.send_bot_message(self.nickname)
        elif message.find('No proof against') != -1:
            print(f"think I've cracked it")
            self.send_bot_message("y")
        elif message.find("has disapproved") == -1 and message.find(' has joined') == -1 and message.find(' has ') != -1:
            print(f"Been shown a card")
            self.useShownCard(message)
        elif message.find('Want to enter in a room') != -1:
            print(f"Saying yes to enter a room")
            self.send_bot_message("y")
        elif message.find('Choose a room to enter:') != -1:
            print(f"Choosing a room")
            self.chooseRoom()
        elif message.find('6.) Mrs. White') != -1:
            print(f"Choosing suspect and weapon")
            self.chooseSuspectAndWeapon()
        elif message.find('Your Cards') != -1 and not self.remembered_cards:
            print(f"Eliminating my cards from possible answer")
            self.remember_cards(message)
        elif message.find('Do you want to revel cards') != -1:
            print(f"I'm don't know enough to revel cards, if only I was smarter")
            self.send_bot_message("n")
        elif message.find('Roll Dice') != -1:
            print(f"Trying to roll dice")
            self.send_bot_message("y")
        elif message.find('Invalid room selected!') != -1:
            print(f"OOOOPS choosing room")
            self.chooseRoom()

        return None

    pass


if __name__ == "__main__":
    bot = Cluedobot()
