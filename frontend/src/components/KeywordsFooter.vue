<template>
  <footer class="keywords-section">
    <h3 class="keywords-title">Palabras clave populares:</h3>
    <div class="keywords-list">
      <span 
        v-for="(count, keyword) in keywords" 
        :key="keyword"
        class="keyword"
        @click="handleKeywordClick(keyword)"
      >
        {{ keyword }} ({{ count }})
      </span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'KeywordsFooter',
  props: {
    keywords: {
      type: Object,
      required: true
    }
  },
  methods: {
    handleKeywordClick(keyword) {
      this.$emit('keyword-selected', keyword);
    }
  }
}
</script>

<style scoped>
.keywords-section {
  background: #16213e;
  padding: 20px;
  border-radius: 10px;
  margin-top: 40px;
}

.keywords-title {
  margin-bottom: 15px;
  color: #e94560;
}

.keywords-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.keyword {
  background: #0f3460;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.keyword:hover {
  background: #e94560;
}
</style>