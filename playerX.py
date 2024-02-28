import socket

def main():
    HOST = 'localhost'
    PORT = 5000 

    #create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #send player X's connection request to the server
    client_socket.sendto(b"Player X", (HOST, PORT))

    while True:
        #receive server messages
        message, _ = client_socket.recvfrom(1024)
        print(message.decode())

        #if it's the player's turn, allow them to make a move
        if "Your turn" in message.decode():
            move = input("Enter your move (row,col): ")
            client_socket.sendto(move.encode(), (HOST, PORT))

            #receive updated board from server
            board, _ = client_socket.recvfrom(1024)
            print("Updated board:")
            print(eval(board.decode()))

            #check if the game is over
            game_status, _ = client_socket.recvfrom(1024)
            print(game_status.decode())
            break

    #close the socket
    client_socket.close()

if __name__ == "__main__":
    main()
