import { ref, computed } from 'vue'

// Estado global reactivo
const authState = ref({
  isAuthenticated: !!localStorage.getItem('authToken'),
  user: JSON.parse(localStorage.getItem('user') || 'null')
})

// Métodos para actualizar el estado
export function useAuth() {
  const setAuth = (token, userData) => {
    localStorage.setItem('authToken', token)
    localStorage.setItem('user', JSON.stringify(userData))
    authState.value.isAuthenticated = true
    authState.value.user = userData
    
    // Disparar evento personalizado para notificar a todos los componentes
    window.dispatchEvent(new CustomEvent('auth-state-changed', { 
      detail: { isAuthenticated: true, user: userData } 
    }))
  }

  const clearAuth = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    authState.value.isAuthenticated = false
    authState.value.user = null
    
    window.dispatchEvent(new CustomEvent('auth-state-changed', { 
      detail: { isAuthenticated: false, user: null } 
    }))
  }

  const isAuthenticated = computed(() => authState.value.isAuthenticated)
  const currentUser = computed(() => authState.value.user)
  const isAdmin = computed(() => authState.value.user?.is_admin || false)

  return {
    isAuthenticated,
    currentUser,
    isAdmin,
    setAuth,
    clearAuth
  }
}