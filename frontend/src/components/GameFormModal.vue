<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <h2>{{ game ? 'Editar Juego' : 'Agregar Nuevo Juego' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Nombre:</label>
          <input v-model="form.name" type="text" required>
        </div>
        
        <div class="form-group">
          <label>Descripción:</label>
          <textarea v-model="form.description" required rows="4"></textarea>
        </div>
        
        <div class="form-group">
          <label>Año:</label>
          <input v-model="form.year" type="number" min="1950" :max="currentYear" required>
        </div>
        
        <div class="form-group">
          <label>URL de Imagen:</label>
          <input v-model="form.image" type="url">
        </div>
        
        <div class="form-group">
          <label>URL del Juego:</label>
          <input v-model="form.url" type="url">
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
          <button type="button" @click="close" class="btn-cancel">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'GameFormModal',
  props: {
    show: Boolean,
    game: Object
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const form = ref({
      name: '',
      description: '',
      year: new Date().getFullYear(),
      image: '',
      url: ''
    })
    const loading = ref(false)
    const error = ref('')
    const currentYear = new Date().getFullYear()

    watch(() => props.game, (newGame) => {
      if (newGame) {
        form.value = { ...newGame }
      } else {
        form.value = {
          name: '',
          description: '',
          year: new Date().getFullYear(),
          image: '',
          url: ''
        }
      }
      error.value = ''
    }, { immediate: true })

    const handleSubmit = () => {
      loading.value = true
      error.value = ''
      
      if (form.value.year < 1950 || form.value.year > currentYear) {
        error.value = `El año debe estar entre 1950 y ${currentYear}`
        loading.value = false
        return
      }
      
      emit('save', form.value)
      loading.value = false
    }

    const close = () => {
      emit('close')
    }

    return {
      form,
      loading,
      error,
      currentYear,
      handleSubmit,
      close
    }
  }
}
</script>