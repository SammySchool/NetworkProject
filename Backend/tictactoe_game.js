class Player {
    constructor(label, conn) {
        this.label = label;
        this.conn = conn; // This can be an ID or a WebSocket connection reference
    }
}

class Move {
    constructor(row, col, label = "") {
        this.row = row;
        this.col = col;
        this.label = label;
    }
}

const BOARD_SIZE = 3;

class TicTacToeGame {
    constructor(boardSize = 3) {
        this.boardSize = boardSize;
        this.players = []; // This will hold Player objects which include the connection
        this.currentMoves = Array.from({ length: boardSize }, () => Array(boardSize).fill(null));
        this.currentPlayerIndex = 0;
        this.hasWinner = false;
        this.winnerCombo = [];
    }

    addPlayer(conn) {
        if (this.players.length < 2) {
            const playerLabel = this.players.length === 0 ? 'X' : 'O';
            const player = new Player(playerLabel, conn);
            this.players.push(player);
            return this.players.length - 1; // Return player ID
        }
        return null; // No more players can be added
    }

    processMove(move, playerID) {
        if (this.hasWinner || this.currentPlayerIndex !== playerID) {
            return { valid: false, status: "" };
        }
        const { row, col } = move;
        if (this.currentMoves[row][col] !== null) {
            return { valid: false, status: "" }; // Invalid move
        }
        this.currentMoves[row][col] = move.label;
        if (this.checkWinner()) {
            this.hasWinner = true;
            return { valid: true, status: "WIN" };
        }
        if (this.checkTie()) {
            return { valid: true, status: "TIE" };
        }
        this.togglePlayer();
        return { valid: true, status: "" };
    }

    checkWinner() {
        // Check rows, columns, and diagonals for a win
        const lines = [
            ...this.currentMoves,
            ...this.currentMoves[0].map((_, i) => this.currentMoves.map(row => row[i])), // Columns
            this.currentMoves.map((row, i) => row[i]), // Diagonal
            this.currentMoves.map((row, i) => row[this.boardSize - 1 - i]) // Anti-diagonal
        ];
        for (let line of lines) {
            if (line.every(cell => cell === line[0] && cell !== null)) {
                return true;
            }
        }
        return false;
    }

    checkTie() {
        return this.currentMoves.every(row => row.every(cell => cell !== null));
    }

    togglePlayer() {
        this.currentPlayerIndex = (this.currentPlayerIndex + 1) % 2;
    }

    resetGame() {
        this.currentMoves = Array.from({ length: this.boardSize }, () => Array(this.boardSize).fill(null));
        this.currentPlayerIndex = 0;
        this.hasWinner = false;
        this.winnerCombo = [];
    }
}

module.exports = { TicTacToeGame, Player, Move }; // Export for use in other modules or AWS Lambda functions
