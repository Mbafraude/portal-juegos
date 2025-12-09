from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .init import db
from .models import User, Game

# Blueprints
games_bp = Blueprint('games', __name__)
auth_bp = Blueprint('auth', __name__)

# Rutas de autenticación
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'El usuario ya existe'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        is_admin=data.get('is_admin', False)
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuario creado exitosamente',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

# Rutas de juegos
@games_bp.route('/', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify({
        'games': [game.to_dict() for game in games],
        'total': len(games)
    }), 200

@games_bp.route('/', methods=['POST'])
@jwt_required()
def create_game():
    data = request.get_json()
    
    required_fields = ['name', 'description', 'year']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    game = Game(
        name=data['name'],
        description=data['description'],
        year=data['year'],
        image=data.get('image', ''),
        url=data.get('url', ''),
        user_id=get_jwt_identity()
    )
    
    db.session.add(game)
    db.session.commit()
    
    return jsonify({
        'message': 'Juego creado exitosamente',
        'game': game.to_dict()
    }), 201

@games_bp.route('/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.get_json()
    
    # Actualizar campos
    if 'name' in data:
        game.name = data['name']
    if 'description' in data:
        game.description = data['description']
    if 'year' in data:
        game.year = data['year']
    if 'image' in data:
        game.image = data['image']
    if 'url' in data:
        game.url = data['url']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Juego actualizado exitosamente',
        'game': game.to_dict()
    }), 200

@games_bp.route('/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    
    db.session.delete(game)
    db.session.commit()
    
    return jsonify({'message': 'Juego eliminado exitosamente'}), 200