import asyncio
import tkinter as tk
import websockets
from tic_tac_toe import Move
from tkinter import font, messagebox

class TicTacToeBoard(tk.Tk):
    def __init__(self, server_address, server_port):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self.server_address = server_address
        self.server_port = server_port
        self.websocket = None
        self.create_widgets()
        self.disable_board()
        asyncio.run(self.connect_to_server())

    async def connect_to_server(self):
        uri = f"ws://{self.server_address}:{self.server_port}"
        self.websocket = await websockets.connect(uri)
        asyncio.create_task(self.listen_to_server())

    async def send_move_to_server(self, row, col):
        self.disable_board()
        await self.websocket.send(f"{row}:{col}")

    async def listen_to_server(self):
        try:
            async for message in self.websocket:
                # Similar logic for handling messages from the server
                pass
        except websockets.exceptions.ConnectionClosed:
            self.after(0, lambda: messagebox.showerror("Connection Error", "Lost connection to the server."))

    # Additional methods and tkinter setup as before

def main():
    server_address = '0.0.0.0'  
    server_port = 5555
    app = TicTacToeBoard(server_address, server_port)
    app.mainloop()

if __name__ == "__main__":
    main()
