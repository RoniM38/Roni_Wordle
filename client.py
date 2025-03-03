import socket
from rich import print as rprint
from comm_utils import comm_utils

class Client:
    DEFAULT_PORT = 12345
    LOCALHOST = '127.0.0.1'

    def __init__(self, server_ip=LOCALHOST, port=DEFAULT_PORT):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, port))
        self.attempts = 0
    
    def in_list(self, attempted_word):
        with open("words.txt", "r") as f:
            for line in f.readlines():
                if line.strip() == attempted_word:
                    return True
        return False

    def play(self):
        while True:
            response = comm_utils.receive_message(self.client_socket)
            if response is None:
                break
            rprint(response)

            if (response.lower()).count("green") == 5 or self.attempts >= 6:
                while True:
                    extra_message = comm_utils.receive_message(self.client_socket)
                    if extra_message is None:
                        break
                    rprint(extra_message)  # Print any additional messages
                self.client_socket.close()
                return

            keyboard = comm_utils.receive_message(self.client_socket)
            if keyboard is None:
                break
            rprint(keyboard)

            while True:
                guess = input("Enter your guess: ").strip().lower()
                is_valid = self.in_list(guess)
                if len(guess) == 5 and guess.isalpha() and is_valid:
                    self.attempts += 1
                    comm_utils.send_message(self.client_socket, guess)
                    break
                elif len(guess) != 5 or not guess.isalpha():
                    rprint("[red]Invalid input! Your guess must be exactly 5 letters.[/]")
                else:
                    rprint("[red]Invalid word. Please guess a word from the word list.[/]")

        self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    client.play()
