import apiClient from '../config/axios'
import { useAuth } from '../store/authStore'

// Obtener funciones del store
const authStore = useAuth()

class AuthService {
  async register(userData) {
    try {
      const response = await apiClient.post('/auth/register', userData)
      
      // Si el registro incluye login automático, establecer auth
      if (response.data.access_token) {
        authStore.setAuth(response.data.access_token, response.data.user)
      }
      
      return response.data
    } catch (error) {
      throw new Error(`Error en registro: ${error.response?.data?.error || error.message}`)
    }
  }

  async login(credentials) {
    try {
      const response = await apiClient.post('/auth/login', credentials)
      
      if (response.data.access_token) {
        authStore.setAuth(response.data.access_token, response.data.user)
      }
      
      return response.data
    } catch (error) {
      throw new Error(`Error en login: ${error.response?.data?.error || error.message}`)
    }
  }

  logout() {
    authStore.clearAuth()
    // No recargamos la página inmediatamente, dejamos que los componentes reaccionen
  }

  getCurrentUser() {
    return authStore.currentUser.value
  }

  isAuthenticated() {
    return authStore.isAuthenticated.value
  }

  isAdmin() {
    return authStore.isAdmin.value
  }
}

export default new AuthService()