from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # Configuración desde variables de entorno
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-temporal')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-clave-secreta')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://portal_user:portal_password@localhost:5432/portal_juegos')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Importar y registrar blueprints
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.games_bp, url_prefix='/api/games')
        app.register_blueprint(routes.auth_bp, url_prefix='/api/auth')
    
    return app