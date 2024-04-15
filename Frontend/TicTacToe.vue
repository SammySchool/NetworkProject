<template>
  <div id="game">
    <h1>Tic-Tac-Toe Game</h1>
    <div v-if="playerId">
      <h2>You are Player {{ playerId }}</h2>
      <div v-for="row in 3" :key="row" class="board-row">
        <button v-for="col in 3" :key="col" @click="makeMove(row-1, col-1)" :disabled="!isActive || board[row-1][col-1]">{{ board[row-1][col-1] }}</button>
      </div>
    </div>
    <h2 v-if="status">{{ status }}</h2>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      socket: null,
      board: Array(3).fill().map(() => Array(3).fill('')),
      playerId: null,
      isActive: false,
      status: '',
    };
  },
  mounted() {
    this.socket = io('http://localhost:5555'); // Connect to the Socket.IO server
    this.socket.on('player_id', data => {
      this.playerId = data.id;
      this.isActive = this.playerId === 1;
    });
    this.socket.on('move_made', data => {
      this.board[data.row][data.col] = data.label;
      this.isActive = data.label !== this.playerId;
    });
    this.socket.on('game_status', data => {
      this.status = data.status;
      this.isActive = false; // Disable further moves if game is over
    });
    this.socket.emit('register');
  },
  methods: {
    makeMove(row, col) {
      if (this.isActive && !this.board[row][col]) {
        this.socket.emit('make_move', { row: row, col: col, playerId: this.playerId - 1 });
      }
    }
  }
}
</script>

<style>
.board-row {
  display: flex;
}
button {
  width: 60px;
  height: 60px;
  font-size: 2em;
  margin: 5px;
  cursor: pointer;
}
</style>
