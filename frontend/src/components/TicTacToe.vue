<template>
  <div v-if="show" class="tic-tac-toe-modal">
    <div class="tic-tac-toe-container">
      <h2>Tres en Raya</h2>
      <div class="game-status">{{ gameStatus }}</div>
      <div class="tic-tac-toe-board">
        <div 
          v-for="(cell, index) in board" 
          :key="index"
          class="cell"
          @click="makeMove(index)"
        >
          {{ cell }}
        </div>
      </div>
      <div>
        <button @click="resetGame">Reiniciar Juego</button>
        <button class="close-btn" @click="close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TicTacToe',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      board: Array(9).fill(''),
      currentPlayer: 'X',
      gameStatus: 'Turno del jugador X',
      gameOver: false
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.resetGame();
      }
    }
  },
  methods: {
    makeMove(index) {
      if (this.board[index] || this.gameOver) return;
      
      this.board[index] = this.currentPlayer;
      
      if (this.checkWinner()) {
        this.gameStatus = `¡Jugador ${this.currentPlayer} gana!`;
        this.gameOver = true;
        return;
      }
      
      if (this.checkTie()) {
        this.gameStatus = '¡Empate!';
        this.gameOver = true;
        return;
      }
      
      this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
      this.gameStatus = `Turno del jugador ${this.currentPlayer}`;
    },
    
    checkWinner() {
      const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columnas
        [0, 4, 8], [2, 4, 6] // Diagonales
      ];
      
      return winPatterns.some(pattern => {
        const [a, b, c] = pattern;
        return this.board[a] && 
               this.board[a] === this.board[b] && 
               this.board[a] === this.board[c];
      });
    },
    
    checkTie() {
      return this.board.every(cell => cell !== '');
    },
    
    resetGame() {
      this.board = Array(9).fill('');
      this.currentPlayer = 'X';
      this.gameStatus = 'Turno del jugador X';
      this.gameOver = false;
    },
    
    close() {
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.tic-tac-toe-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.tic-tac-toe-container {
  background: #16213e;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.tic-tac-toe-board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
  margin: 20px 0;
  background: #0f3460;
  padding: 5px;
  border-radius: 10px;
}

.cell {
  aspect-ratio: 1;
  background: #16213e;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.cell:hover {
  background: #1a3a6e;
}

.game-status {
  margin: 15px 0;
  font-size: 1.1rem;
  color: #e94560;
}
</style>

