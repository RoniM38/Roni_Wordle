import socket
from select import select
import random
from rich import print as rprint
from comm_utils import comm_utils

class Server:
    MAX_CLIENTS = 8
    DEFAULT_PORT = 12345
    MAX_ATTEMPTS = 6

    def __init__(self, host='0.0.0.0', port=DEFAULT_PORT, max_clients=MAX_CLIENTS):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(max_clients)

        self.clients = {}
        self.word_list = self.load_word_list()
        print(f"Server listening on {host}:{port}")

    def load_word_list(self):
        with open('words.txt', 'r') as file:
            return {word.strip() for word in file.readlines()}

    def generate_word(self):
        return random.choice(list(self.word_list))

    def check_word(self, guessed_word, goal_word, guessed_letters):
        feedback = []
        goal_word_list = list(goal_word)

        for i, letter in enumerate(guessed_word):
            if letter == goal_word[i]:
                feedback.append(f"[green]{letter}[/]")
                guessed_letters[letter] = "green"
                goal_word_list[i] = None  
            elif letter in goal_word_list:
                feedback.append(f"[yellow]{letter}[/]")
                if guessed_letters.get(letter) != "green":
                    guessed_letters[letter] = "yellow"
                goal_word_list[goal_word_list.index(letter)] = None
            else:
                feedback.append(f"[red]{letter}[/]")
                guessed_letters[letter] = "red"

        return " ".join(feedback)

    def format_keyboard(self, guessed_letters):
        keyboard = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            color = "red" if guessed_letters.get(letter) == "red" else guessed_letters.get(letter, "white")
            keyboard.append(f"[{color}]{letter}[/]")
        return " ".join(keyboard)

    def run(self):
        inputs = [self.server_socket]

        while True:
            readable, _, _ = select(inputs, [], [])

            for s in readable:
                if s is self.server_socket:
                    client_socket, addr = self.server_socket.accept()
                    print(f"New connection from {addr}")

                    goal_word = self.generate_word()
                    print(goal_word)
                    self.clients[client_socket] = {"goal_word": goal_word, "attempts": 0, "guessed_letters": {}}

                    comm_utils.send_message(client_socket, "Welcome to Wordle! Guess a 5-letter word:")
                    comm_utils.send_message(client_socket, self.format_keyboard({}))
                    inputs.append(client_socket)
                else:
                    try:
                        client_data = self.clients[s]
                        msg = comm_utils.receive_message(s)
                        if not msg:
                            raise ConnectionResetError
                        
                        result = self.check_word(msg, client_data["goal_word"], client_data["guessed_letters"])
                        keyboard = self.format_keyboard(client_data["guessed_letters"])

                        comm_utils.send_message(s, result)
                        comm_utils.send_message(s, keyboard)

                        if msg == client_data["goal_word"]:
                            print(f"Player won! Word: {msg}")
                            comm_utils.send_message(s, "You win! Game over.")
                            self.disconnect_client(s, inputs)
                            continue
                        
                        client_data["attempts"] += 1
                        if client_data["attempts"] >= self.MAX_ATTEMPTS:
                            print(f"Player lost! Word was {client_data['goal_word']}")
                            comm_utils.send_message(s, f"You lose! The word was {client_data['goal_word']}")
                            comm_utils.send_message(s, "Game over. Please rejoin to play again.")
                            self.disconnect_client(s, inputs)
                            continue

                    except (ConnectionResetError, OSError):
                        print("Client disconnected")
                        self.disconnect_client(s, inputs)

    def disconnect_client(self, s, inputs):
        if s in self.clients:
            del self.clients[s]
        if s in inputs:
            inputs.remove(s)
        s.close()

if __name__ == "__main__":
    server = Server()
    server.run()
