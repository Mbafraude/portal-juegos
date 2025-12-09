<template>
  <div class="game-card" @click="handleClick">
    <img :src="game.image || '/default-game.jpg'" :alt="game.name" class="game-image">
    <div class="game-info">
      <h3 class="game-title">{{ game.name }}</h3>
      <p class="game-year">Año: {{ game.year }}</p>
      <p class="game-description">{{ truncatedDescription }}</p>
      
      <div class="game-actions" v-if="isAdmin">
        <button @click.stop="handleEdit" class="btn-edit">✏️ Editar</button>
        <button @click.stop="handleDelete" class="btn-delete">🗑️ Eliminar</button>
      </div>
      <button v-else @click.stop="visitGame">Ver más</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameCard',
  props: {
    game: {
      type: Object,
      required: true
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    truncatedDescription() {
      const maxLength = 120;
      return this.game.description.length > maxLength 
        ? this.game.description.substring(0, maxLength) + '...'
        : this.game.description;
    }
  },
  methods: {
    handleClick() {
      this.$emit('game-selected', this.game);
    },
    visitGame() {
      if (this.game.url && this.game.url !== '#') {
        window.open(this.game.url, '_blank');
      }
    },
    handleEdit() {
      this.$emit('edit-game', this.game);
    },
    handleDelete() {
      this.$emit('delete-game', this.game.id);
    }
  }
}
</script>

<style scoped>
.game-card {
  background: #16213e;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.game-card:hover {
  transform: translateY(-5px);
}

.game-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.game-info {
  padding: 15px;
}

.game-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #e94560;
}

.game-year {
  color: #888;
  font-size: 0.9rem;
}

.game-description {
  margin: 10px 0;
  font-size: 0.9rem;
  color: #ccc;
  line-height: 1.4;
}

.game-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn-edit {
  background: #2196F3;
  padding: 8px 12px;
  font-size: 0.8rem;
}

.btn-delete {
  background: #f44336;
  padding: 8px 12px;
  font-size: 0.8rem;
}
</style>