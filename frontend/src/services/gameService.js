import apiClient from '../config/axios'

class GameService {
  // Obtener todos los juegos con filtros
  async getGames(params = {}) {
    try {
      const response = await apiClient.get('/games/', { params })
      return response.data
    } catch (error) {
      throw new Error(`Error al obtener juegos: ${error.response?.data?.error || error.message}`)
    }
  }

  // Obtener un juego por ID
  async getGameById(id) {
    try {
      const response = await apiClient.get(`/games/${id}`)
      return response.data
    } catch (error) {
      throw new Error(`Error al obtener el juego: ${error.response?.data?.error || error.message}`)
    }
  }

  // Crear un nuevo juego
  async createGame(gameData) {
    try {
      const response = await apiClient.post('/games/', gameData)
      return response.data
    } catch (error) {
      throw new Error(`Error al crear el juego: ${error.response?.data?.error || error.message}`)
    }
  }

  // Actualizar un juego
  async updateGame(id, gameData) {
    try {
      const response = await apiClient.put(`/games/${id}`, gameData)
      return response.data
    } catch (error) {
      throw new Error(`Error al actualizar el juego: ${error.response?.data?.error || error.message}`)
    }
  }

  // Eliminar un juego
  async deleteGame(id) {
    try {
      const response = await apiClient.delete(`/games/${id}`)
      return response.data
    } catch (error) {
      throw new Error(`Error al eliminar el juego: ${error.response?.data?.error || error.message}`)
    }
  }
}

export default new GameService()