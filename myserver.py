import asyncio
import websockets
from tictactoe_game import TicTacToeGame, Player, Move

async def handle_client(websocket, path, game):
    player_id = game.add_player(websocket)
    if player_id is not None:
        await websocket.send(f"PLAYER {player_id + 1}")
        try:
            async for message in websocket:
                print(f"Received move: {message}")
                row, col = map(int, message.split(':'))
                valid_move, game_status = game.process_move(Move(row, col, game.players[player_id].label), player_id)
                if valid_move:
                    await broadcast(f"MOVE {row} {col} {game.players[player_id].label}", game)
                    if game_status != "":
                        await broadcast(game_status, game)
                        game.reset_game()
                else:
                    await websocket.send("INVALID MOVE")
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        finally:
            game.remove_player(player_id)

async def broadcast(message, game):
    for player in game.players:
        if player.conn:
            await player.conn.send(message)

async def main():
    game = TicTacToeGame()
    async with websockets.serve(lambda ws, path: handle_client(ws, path, game), '0.0.0.0', 5555):
        print("Server started. Waiting for players...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
