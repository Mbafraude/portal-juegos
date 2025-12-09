# Portal de Videojuegos 

Aplicación completa de portal de videojuegos con frontend Vue.js y backend Flask.

## Características

-  Listar videojuegos desde PostgreSQL
-  Buscar y filtrar juegos
-  Jugar al Tres en Raya
-  Autenticación JWT
-  CRUD completo de juegos (solo administradores)
-  API RESTful
-  Permite subir imágenes de los juegos a través de links externos (url de imagen)

## Instalación

### Backend
en la terminal
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar PostgreSQL y ejecutar:
psql -f setup_database.sql

python create_tables.py
python run.py

### frontend
abrir nuevo terminal (sin cerrar el anterior)
cd frontend
npm run dev

##Portal de juegos
Cuenta de administrador:
Usuario:admin
Contraseña: admin123
