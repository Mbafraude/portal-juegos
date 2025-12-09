<template>
  <div>
    <h1>Gestión de Usuarios</h1>
    
    <!-- Formulario para crear usuario -->
    <div style="border: 1px solid #ccc; padding: 20px; margin: 20px 0;">
      <h2>Crear Usuario Nuevo</h2>
      <form @submit.prevent="crearUsuario">
        <div style="margin: 10px 0;">
          <input 
            v-model="nuevoUsuario.firstName" 
            placeholder="Nombre" 
            required
            style="padding: 8px; margin: 5px; width: 200px;"
          >
          <input 
            v-model="nuevoUsuario.lastName" 
            placeholder="Apellido" 
            required
            style="padding: 8px; margin: 5px; width: 200px;"
          >
        </div>
        <div style="margin: 10px 0;">
          <input 
            v-model="nuevoUsuario.email" 
            type="email" 
            placeholder="Email" 
            required
            style="padding: 8px; margin: 5px; width: 420px;"
          >
        </div>
        <div style="margin: 10px 0;">
          <input 
            v-model="nuevoUsuario.phone" 
            placeholder="Teléfono (opcional)"
            style="padding: 8px; margin: 5px; width: 420px;"
          >
        </div>
        <div style="margin: 10px 0;">
          <input 
            v-model="nuevoUsuario.age" 
            type="number" 
            placeholder="Edad (opcional)"
            style="padding: 8px; margin: 5px; width: 420px;"
          >
        </div>
        <button type="submit" :disabled="creando" style="padding: 10px 20px; margin: 5px;">
          {{ creando ? 'Creando...' : 'Crear Usuario' }}
        </button>
      </form>
      <p v-if="mensaje" style="color: green; margin: 10px 5px;">{{ mensaje }}</p>
    </div>

    <!-- Lista de usuarios -->
    <div>
      <h2>Lista de Usuarios (Total: {{ usuarios.length }})</h2>
      
      <div v-if="cargando">
        <p>Cargando usuarios...</p>
      </div>
      
      <div v-else-if="error">
        <p style="color: red;">Error: {{ error }}</p>
      </div>
      
      <div v-else>
        <div 
          v-for="usuario in usuarios" 
          :key="usuario.id" 
          style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; background: white;"
        >
          <h3 style="margin: 0 0 10px 0;">{{ usuario.firstName }} {{ usuario.lastName }}</h3>
          <p style="margin: 5px 0;"><strong>Email:</strong> {{ usuario.email }}</p>
          <p style="margin: 5px 0;"><strong>ID:</strong> {{ usuario.id }}</p>
          <p v-if="usuario.phone" style="margin: 5px 0;"><strong>Teléfono:</strong> {{ usuario.phone }}</p>
          <p v-if="usuario.age" style="margin: 5px 0;"><strong>Edad:</strong> {{ usuario.age }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      usuarios: [],
      cargando: false,
      error: null,
      creando: false,
      mensaje: '',
      nuevoUsuario: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        age: ''
      },
      siguienteId: 100
    }
  },
  mounted() {
    this.obtenerUsuarios()
  },
  methods: {
    async obtenerUsuarios() {
      this.cargando = true
      this.error = null
      
      try {
        const respuesta = await this.$axios.get('/users')
        this.usuarios = respuesta.data.users
        // Encontrar el ID más alto para continuar desde ahí
        const maxId = Math.max(...this.usuarios.map(u => u.id))
        this.siguienteId = maxId + 1
      } catch (error) {
        this.error = 'No se pudieron cargar los usuarios: ' + error.message
        console.error('Error:', error)
      } finally {
        this.cargando = false
      }
    },
    
    async crearUsuario() {
      this.creando = true
      this.mensaje = ''
      
      try {
        // Llamar a la API para simular la creación
        const respuesta = await this.$axios.post('/users/add', this.nuevoUsuario)
        
        // Crear un objeto usuario completo con ID único
        const usuarioCreado = {
          ...respuesta.data,
          id: this.siguienteId, // Usamos nuestro propio ID
          phone: this.nuevoUsuario.phone || undefined,
          age: this.nuevoUsuario.age ? parseInt(this.nuevoUsuario.age) : undefined
        }
        
        // Agregar el usuario al principio de la lista
        this.usuarios.unshift(usuarioCreado)
        
        // Incrementar el ID para el próximo usuario
        this.siguienteId++
        
        this.mensaje = `Usuario ${usuarioCreado.firstName} ${usuarioCreado.lastName} creado correctamente!`
        
        // Limpiar el formulario
        this.nuevoUsuario = {
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
          age: ''
        }
        
      } catch (error) {
        this.mensaje = 'Error al crear el usuario: ' + error.message
        console.error('Error:', error)
      } finally {
        this.creando = false
      }
    }
  }
}
</script>

<style>
body {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
}

input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

h1 {
  color: #333;
  text-align: center;
}

h2 {
  color: #555;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 5px;
}
</style>