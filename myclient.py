import socket
import threading
import tkinter as tk
from tkinter import messagebox, font

class TicTacToeBoard(tk.Tk):
    def __init__(self, server_address, server_port):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_address, server_port))
        self.player_label = None
        self.create_widgets()
        self.disable_board()
        threading.Thread(target=self.listen_to_server, daemon=True).start()

    def create_widgets(self):
        self.cells = {}
        self.board_frame = tk.Frame(self)
        self.board_frame.pack()
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.board_frame, text='', font=font.Font(size=32), width=5, height=2,
                                   command=lambda r=row, c=col: self.send_move_to_server(r, c))
                button.grid(row=row, column=col)
                self.cells[(row, col)] = button

        self.status_label = tk.Label(self, text="Connecting to server...", font=font.Font(size=20))
        self.status_label.pack(pady=20)

    def disable_board(self):
        for button in self.cells.values():
            button.config(state='disabled')

    def enable_board(self):
        for button in self.cells.values():
            button.config(state='normal')

    def send_move_to_server(self, row, col):
        self.disable_board()
        self.client_socket.sendall(f"{row}:{col}".encode())

    def listen_to_server(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if data.startswith("PLAYER"):
                    self.player_label = data.split()[1]
                    self.status_label.config(text=f"You are Player {self.player_label}")
                elif data.startswith("MOVE"):
                    _, row, col, label = data.split()
                    self.update_board(int(row), int(col), label)
                elif data == "WIN":
                    self.status_label.config(text=f"Player {self.player_label} wins!")
                    messagebox.showinfo("Game Over", f"Player {self.player_label} wins!")
                    self.disable_board()
                elif data == "TIE":
                    self.status_label.config(text="Game Tied!")
                    messagebox.showinfo("Game Over", "Game Tied!")
                    self.disable_board()
                elif data == "INVALID MOVE":
                    messagebox.showerror("Invalid Move", "That move is not allowed.")
                    self.enable_board()
            except ConnectionError:
                messagebox.showerror("Connection Error", "Lost connection to the server.")
                break

    def update_board(self, row, col, label):
        button = self.cells[(row, col)]
        button.config(text=label, state='disabled')
        self.status_label.config(text=f"Player {label}'s turn")
        if label != self.player_label:
            self.enable_board()

def main():
    server_address = '0.0.0.0'  
    server_port = 5555
    app = TicTacToeBoard(server_address, server_port)
    app.mainloop()

if __name__ == "__main__":
    main()
