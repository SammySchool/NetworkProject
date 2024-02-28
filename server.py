import socket

#print the Tic-Tac-Toe board
def print_board(board):
    print("  0 1 2")
    for i in range(3):
        print(f"{i} {' '.join(board[i])}")

#check win condition
def check_win(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

#handle the game logic
def play_game(conn1, addr1, conn2, addr2):
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        current_conn = server_socket if current_player == 'X' else conn2
        other_conn = conn2 if current_conn == server_socket else conn1
        current_addr = addr1 if current_conn == server_socket else addr2

        server_socket.sendto(b'Your turn', current_addr)
        server_socket.sendto(b'Opponent\'s turn', addr2) 

        print_board(board)

        server_socket.sendto(str(board).encode(), current_addr)

        #move from the current player
        move_data, _ = current_conn.recvfrom(1024)
        move = tuple(map(int, move_data.decode().split(',')))

        #move is valid
        if board[move[0]][move[1]] != " ":
            server_socket.sendto(b'Invalid move. Try again.', current_addr)
            continue

        #update the board with the move
        board[move[0]][move[1]] = current_player

        #check for a win or tie
        if check_win(board, current_player):
            server_socket.sendto(b'You win!', current_addr)
            other_conn.sendto(b'You lose!', addr2) 
            break
        elif all(all(cell != " " for cell in row) for row in board):
            server_socket.sendto(b'It\'s a tie!', current_addr)
            other_conn.sendto(b'It\'s a tie!', addr2)  
            break

        #switch player
        current_player = 'O' if current_player == 'X' else 'X'

#main function / server start
def main():
    HOST = ''  
    PORT = 5000  

    #create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #b
    server_socket.bind((HOST, PORT))

    print("Server started...")

    # Accept two connections
    conn1, addr1 = server_socket.recvfrom(1024)
    conn2, addr2 = server_socket.recvfrom(1024)

    print("Connected to:", addr1)
    print("Connected to:", addr2)

    #start game
    play_game(conn1, addr1, conn2, addr2)  

    #close the server socket
    server_socket.close()

if __name__ == "__main__":
    main()

