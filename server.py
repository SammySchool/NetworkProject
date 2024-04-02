import socket
import threading

# Global variables for the game state
current_player = 'X'
board = [[' ']*3 for _ in range(3)]
players = {}
player_order = []

def handle_client(conn, addr):
    global current_player

    player_mark = conn.recv(1024).decode()
    players[player_mark] = conn
    player_order.append(player_mark)
    print(f"Player {player_mark} connected from {addr}")

    conn.send("Welcome to Tic Tac Toe! Waiting for other player...".encode())

    if len(players) == 2:
        for player in players.values():
            try:
                player.send("Both players connected. Game starting...\n".encode())
            except BrokenPipeError:
                print(f"Error sending data to {player}: Broken pipe")

        while True:
            for player in player_order:
                conn = players[player]
                try:
                    conn.sendall(f"Your turn. Current board state:\n{format_board()}".encode())
                    conn.send("Enter your move (row:col): ".encode())
                except BrokenPipeError:
                    print(f"Error sending data to {player}: Broken pipe")
                    continue

                move = conn.recv(1024).decode().strip()
                if not move:
                    print("No move data received from Player", player)
                    continue

                try:
                    row, col = map(int, move.split(':'))
                except ValueError:
                    print("Invalid move format received from Player", player)
                    continue

                if board[row][col] == ' ':
                    board[row][col] = current_player
                    current_player = 'X' if current_player == 'O' else 'O'
                    winner = check_win()
                    if winner:
                        send_to_all(f"Player {winner} wins!\n{format_board()}")
                        reset_game()
                        break
                    elif check_tie():
                        send_to_all(f"It's a tie!\n{format_board()}")
                        reset_game()
                        break
                    else:
                        send_to_all(f"Move made by Player {player}.\n{format_board()}")
                else:
                    conn.send("Invalid move. Try again.".encode())


def send_to_all(message):
    for conn in players.values():
        conn.send(message.encode())

def format_board():
    return '\n'.join([' '.join(row) for row in board])

def check_win():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def check_tie():
    return all(cell != ' ' for row in board for cell in row)

def reset_game():
    global current_player, board
    current_player = 'X'
    board = [[' ']*3 for _ in range(3)]

def main():
    host = '0.0.0.0'
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Server listening on port", port)

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()