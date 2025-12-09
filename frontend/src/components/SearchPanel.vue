<template>
  <section class="search-section">
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="Buscar juegos por nombre o descripción..."
        @input="handleSearch"
      >
      <select v-model="sortOrder" @change="handleSort">
        <option value="">Ordenar por...</option>
        <option value="asc">Año (Más antiguo primero)</option>
        <option value="desc">Año (Más reciente primero)</option>
      </select>
    </div>
    <p>Mostrando {{ gameCount }} juegos</p>
  </section>
</template>

<script>
export default {
  name: 'SearchPanel',
  emits: ['search', 'sort'],
  data() {
    return {
      searchTerm: '',
      sortOrder: ''
    }
  },
  props: {
    gameCount: {
      type: Number,
      required: true
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.searchTerm);
    },
    handleSort() {
      this.$emit('sort', this.sortOrder);
    }
  }
}
</script>

<style scoped>
.search-section {
  background: #16213e;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

input, select {
  padding: 10px;
  border: none;
  border-radius: 5px;
  background: #0f3460;
  color: white;
  flex: 1;
  min-width: 200px;
}
</style>