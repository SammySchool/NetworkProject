const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { TicTacToeGame, Player, Move } = require('./tictactoe');

const app = express();
const server = http.createServer(app);
const io = socketIo(server); // Setup Socket.io for real-time communication

const game = new TicTacToeGame();

app.use(express.static('path_to_frontend_dist')); // Serve your static Vue.js app

io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    socket.on('register', () => {
        const playerID = game.addPlayer(socket.id);
        if (playerID !== null) {
            io.to(socket.id).emit('player_id', { id: playerID + 1 });
        }
    });

    socket.on('make_move', (data) => {
        const { row, col, playerId } = data;
        const move = new Move(row, col, game.players[playerId].label);
        const result = game.processMove(move, playerId);

        if (result.valid) {
            io.emit('move_made', { row: row, col: col, label: move.label });
            if (result.status) {
                io.emit('game_status', { status: result.status });
            }
        }
    });
});

server.listen(5555, () => {
    console.log('Server is running on port 5555');
});
