<template>
  <div class="container">
    <header>
      <h1>🎮 Portal de Juegos</h1>
      <p>Descubre y juega a los mejores títulos</p>
      
      <div class="user-panel" v-if="isAuthenticated">
        <span>Bienvenido, {{ currentUser?.username }}</span>
        <button v-if="isAdmin" @click="showGameForm = true" class="btn-add">➕ Agregar Juego</button>
        <button @click="logout" class="btn-logout">Cerrar Sesión</button>
      </div>
      <div v-else class="auth-buttons">
        <button @click="showLoginForm = true" class="btn-login">Iniciar Sesión</button>
        <button @click="showRegisterForm = true" class="btn-register">Registrarse</button>
      </div>
    </header>
    
    <SearchPanel 
      :game-count="filteredGames.length"
      @search="handleSearch"
      @sort="handleSort"
    />
    
    <div v-if="loading" class="loading">
      <p>Cargando juegos...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadGames">Reintentar</button>
    </div>
    
    <section v-else class="games-grid">
      <GameCard 
        v-for="game in filteredGames" 
        :key="game.id" 
        :game="game"
        :is-admin="isAdmin"
        @game-selected="handleGameSelect"
        @edit-game="handleEditGame"
        @delete-game="handleDeleteGame"
      />
    </section>
    
    <KeywordsFooter 
      :keywords="keywords"
      @keyword-selected="handleKeywordSelect"
    />
    
    <!-- Modales -->
    <TicTacToe 
      :show="showTicTacToe"
      @close="showTicTacToe = false"
    />
    
    <AuthModal 
      :show="showLoginForm"
      mode="login"
      @close="showLoginForm = false"
      @success="handleAuthSuccess"
    />
    
    <AuthModal 
      :show="showRegisterForm"
      mode="register"
      @close="showRegisterForm = false"
      @success="handleAuthSuccess"
    />
    
    <GameFormModal 
      :show="showGameForm"
      :game="editingGame"
      @close="handleCloseGameForm"
      @save="handleSaveGame"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import GameService from '../services/gameService'
import AuthService from '../services/authService'
import { useAuth } from '../store/authStore'
import GameCard from '../components/GameCard.vue'
import SearchPanel from '../components/SearchPanel.vue'
import KeywordsFooter from '../components/KeywordsFooter.vue'
import TicTacToe from '../components/TicTacToe.vue'
import AuthModal from '../components/AuthModal.vue'
import GameFormModal from '../components/GameFormModal.vue'

export default {
  name: 'HomeView',
  components: {
    GameCard,
    SearchPanel,
    KeywordsFooter,
    TicTacToe,
    AuthModal,
    GameFormModal
  },
  setup() {
    // Usar el store de autenticación
    const { isAuthenticated, currentUser, isAdmin } = useAuth()
    
    // Estado reactivo
    const games = ref([])
    const loading = ref(false)
    const error = ref('')
    const searchTerm = ref('')
    const sortOrder = ref('')
    const showTicTacToe = ref(false)
    const showLoginForm = ref(false)
    const showRegisterForm = ref(false)
    const showGameForm = ref(false)
    const editingGame = ref(null)

    const filteredGames = computed(() => {
      let filtered = games.value
      
      // Filtro por búsqueda
      if (searchTerm.value) {
        const term = searchTerm.value.toLowerCase()
        filtered = filtered.filter(game => 
          game.name.toLowerCase().includes(term) ||
          game.description.toLowerCase().includes(term)
        )
      }
      
      // Ordenamiento
      if (sortOrder.value) {
        filtered = [...filtered].sort((a, b) => {
          return sortOrder.value === 'asc' ? a.year - b.year : b.year - a.year
        })
      }
      
      return filtered
    })

    const keywords = computed(() => {
      const wordCount = {}
      const commonWords = new Set(['el', 'la', 'los', 'las', 'de', 'en', 'y', 'a', 'un', 'una', 'con', 'para'])
      
      games.value.forEach(game => {
        const words = game.description.toLowerCase()
          .replace(/[.,!?;:()]/g, '')
          .split(/\s+/)
          
        words.forEach(word => {
          if (word.length > 3 && !commonWords.has(word)) {
            wordCount[word] = (wordCount[word] || 0) + 1
          }
        })
      })
      
      return Object.entries(wordCount)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10)
        .reduce((obj, [key, value]) => {
          obj[key] = value
          return obj
        }, {})
    })

    // Métodos
    const loadGames = async () => {
      loading.value = true
      error.value = ''
      try {
        const response = await GameService.getGames()
        games.value = response.games
      } catch (err) {
        error.value = err.message
        console.error('Error loading games:', err)
      } finally {
        loading.value = false
      }
    }

    const handleSearch = (term) => {
      searchTerm.value = term
    }

    const handleSort = (order) => {
      sortOrder.value = order
    }

    const handleKeywordSelect = (keyword) => {
      searchTerm.value = keyword
    }

    const handleGameSelect = (game) => {
      const tresEnRayaKeywords = ['tres en raya', 'tictactoe', 'tic tac toe', '3 en raya']
      const isTresEnRaya = tresEnRayaKeywords.some(keyword => 
        game.name.toLowerCase().includes(keyword) ||
        game.description.toLowerCase().includes(keyword)
      )
      
      if (isTresEnRaya) {
        showTicTacToe.value = true
      } else if (game.url && game.url !== '#') {
        window.open(game.url, '_blank')
      }
    }

    const handleEditGame = (game) => {
      editingGame.value = game
      showGameForm.value = true
    }

    const handleDeleteGame = async (gameId) => {
      if (confirm('¿Estás seguro de que quieres eliminar este juego?')) {
        try {
          await GameService.deleteGame(gameId)
          await loadGames() // Recargar la lista
        } catch (err) {
          alert(err.message)
          console.error('Error deleting game:', err)
        }
      }
    }

    const handleCloseGameForm = () => {
      showGameForm.value = false
      editingGame.value = null
    }

    const handleSaveGame = async (gameData) => {
      try {
        if (editingGame.value) {
          await GameService.updateGame(editingGame.value.id, gameData)
        } else {
          await GameService.createGame(gameData)
        }
        await loadGames() // Recargar la lista
        handleCloseGameForm()
      } catch (err) {
        alert(err.message)
        console.error('Error saving game:', err)
      }
    }

    const handleAuthSuccess = () => {
      showLoginForm.value = false
      showRegisterForm.value = false
      loadGames() // Recargar juegos
    }

    const logout = () => {
      AuthService.logout()
      // El store ya se actualizó automáticamente, los componentes reaccionarán
    }

    // Watch para cambios de autenticación (por si acaso)
    watch(isAuthenticated, (newVal) => {
      console.log('Estado autenticación cambiado:', newVal)
      if (newVal) {
        loadGames()
      }
    })

    watch(isAdmin, (newVal) => {
      console.log('Estado admin cambiado:', newVal)
    })

    // Lifecycle
    onMounted(() => {
      loadGames()
      
      // Escuchar eventos de cambio de autenticación
      window.addEventListener('auth-state-changed', () => {
        console.log('Evento auth-state-changed recibido en HomeView')
        loadGames()
      })
    })

    return {
      games,
      loading,
      error,
      searchTerm,
      sortOrder,
      showTicTacToe,
      showLoginForm,
      showRegisterForm,
      showGameForm,
      editingGame,
      isAuthenticated,
      isAdmin,
      currentUser,
      filteredGames,
      keywords,
      handleSearch,
      handleSort,
      handleKeywordSelect,
      handleGameSelect,
      handleEditGame,
      handleDeleteGame,
      handleCloseGameForm,
      handleSaveGame,
      handleAuthSuccess,
      logout,
      loadGames
    }
  }
}
</script>

<style scoped>
.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.user-panel, .auth-buttons {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.btn-add {
  background: #4CAF50;
}

.btn-login {
  background: #2196F3;
}

.btn-register {
  background: #FF9800;
}

.btn-logout {
  background: #f44336;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
}

.error {
  color: #e94560;
}

.error button {
  margin-top: 10px;
  background: #e94560;
}
</style>
