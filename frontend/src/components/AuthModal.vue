<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <h2>{{ mode === 'login' ? 'Iniciar Sesión' : 'Registrarse' }}</h2>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Usuario:</label>
          <input v-model="form.username" type="text" required>
        </div>
        
        <div v-if="mode === 'register'" class="form-group">
          <label>Email:</label>
          <input v-model="form.email" type="email" required>
        </div>
        
        <div class="form-group">
          <label>Contraseña:</label>
          <input v-model="form.password" type="password" required>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="form-actions">
          <button type="submit" :disabled="loading">
            {{ loading ? 'Procesando...' : (mode === 'login' ? 'Iniciar Sesión' : 'Registrarse') }}
          </button>
          <button type="button" @click="close" class="btn-cancel">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AuthService from '../services/authService'

export default {
  name: 'AuthModal',
  props: {
    show: Boolean,
    mode: {
      type: String,
      default: 'login'
    }
  },
  emits: ['close', 'success'],
  setup(props, { emit }) {
    const form = ref({
      username: '',
      email: '',
      password: ''
    })
    const loading = ref(false)
    const error = ref('')

    const handleSubmit = async () => {
      loading.value = true
      error.value = ''
      
      try {
        if (props.mode === 'login') {
          await AuthService.login({
            username: form.value.username,
            password: form.value.password
          })
        } else {
          await AuthService.register(form.value)
        }
        
        // El store ya actualizó el estado automáticamente
        emit('success')
        close()
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const close = () => {
      form.value = { username: '', email: '', password: '' }
      error.value = ''
      emit('close')
    }

    return {
      form,
      loading,
      error,
      handleSubmit,
      close
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #16213e;
  padding: 30px;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #e94560;
}

input {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background: #0f3460;
  color: white;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.error-message {
  color: #e94560;
  margin: 10px 0;
}
</style>