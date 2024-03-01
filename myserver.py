import socket
import threading
from tictactoe_game import TicTacToeGame, Player, Move

def handle_client(conn, addr, game, player_id):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received move from {addr}: {data}")
            row, col = map(int, data.split(':'))
            valid_move, game_status = game.process_move(Move(row, col, game.players[player_id].label), player_id)
            if valid_move:
                broadcast(f"MOVE {row} {col} {game.players[player_id].label}", game)
                if game_status != "":
                    broadcast(game_status, game)
                    game.reset_game()
            else:
                conn.sendall("INVALID MOVE".encode())
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break
    conn.close()

def broadcast(message, game):
    for player in game.players:
        player.conn.sendall(message.encode())

def accept_connections(server_socket, game):
    while len(game.players) < 2:
        conn, addr = server_socket.accept()
        player_id = game.add_player(conn)
        print(f"Player {player_id + 1} connected from {addr}")
        conn.sendall(f"PLAYER {player_id + 1}".encode())
        threading.Thread(target=handle_client, args=(conn, addr, game, player_id)).start()

def server_main():
    host = '0.0.0.0'
    port = 5555
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server started. Waiting for players...")

    game = TicTacToeGame()

    accept_connections(server_socket, game)

if __name__ == "__main__":
    server_main()
