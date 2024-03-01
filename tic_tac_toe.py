import tkinter as tk
from tkinter import font
from typing import NamedTuple
import socket

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = players
        self.board_size = board_size
        self.current_player_index = 0
        self.winner_combo = []
        self._current_moves = [[Move(row, col) for col in range(self.board_size)] for row in range(self.board_size)]
        self._has_winner = False
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        """Toggle between players."""
        self.current_player_index = (self.current_player_index + 1) % len(self._players)

    def is_valid_move(self, move):
        """Check if the move is valid."""
        row, col = move.row, move.col
        return not self._has_winner and self._current_moves[row][col].label == ""

    def process_move(self, move):
        """Process the move and check for a winner."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            if len(results) == 1 and "" not in results:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Check if there is a winner."""
        return self._has_winner

    def is_tied(self):
        """Check if the game is tied."""
        played_moves = (move.label for row in self._current_moves for move in row)
        return not self._has_winner and all(played_moves)

    def reset_game(self):
        """Reset the game."""
        self.current_player_index = 0
        self._has_winner = False
        self.winner_combo = []
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)

class TicTacToeBoard(tk.Tk):
    def __init__(self, game, server_address, server_port):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self.server_address = server_address
        self.server_port = server_port
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                self._cells[button] = (row, col)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def make_move(self, row, col):
        """Handle a player's move."""
        move = Move(row, col, self._game._players[self._game.current_player_index].label)
        if self._game.is_valid_move(move):
            self._update_button(row, col)
            self._game.process_move(move)
            self.client_socket.sendto(f"{row}:{col}".encode(), (self.server_address, self.server_port))
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game._players[self._game.current_player_index].label}" won!'
                color = self._game._players[self._game.current_player_index].color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game._players[self._game.current_player_index].label}'s turn"
                self._update_display(msg)

    def _update_button(self, row, col):
        button = next(btn for btn, (r, c) in self._cells.items() if r == row and c == col)
        button.config(text=self._game._players[self._game.current_player_index].label)
        button.config(fg=self._game._players[self._game.current_player_index].color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    server_address = '0.0.0.0'
    server_port = 5555
    game = TicTacToeGame()
    board = TicTacToeBoard(game, server_address, server_port)
    board.mainloop()
    board.client_socket.close()

if __name__ == "__main__":
    main()
