import sys
import os

<<<<<<< HEAD
# Configurar el path correctamente
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.insert(0, backend_dir)

# Ahora los imports funcionarán
=======
# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

>>>>>>> 507a0ad87c99233659851fe5d37325f93c31083c
from app.init import create_app, db
from app.models import User, Game

app = create_app()

with app.app_context():
    try:
        print("🧪 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas")
        
        # Crear admin
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@portal.com',
                is_admin=True
            )
<<<<<<< HEAD
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Usuario admin creado: admin / admin123")
        else:
            print("✅ Usuario admin ya existe")
        
        # Juegos de ejemplo
        if Game.query.count() == 0:
            games = [
                Game(
                    name='The Legend of Zelda: Breath of the Wild',
                    description='Aventura épica en el reino de Hyrule',
                    year=2017,
                    image='https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=300&fit=crop',
                    url='https://zelda.com',
                    user_id=1
                ),
                Game(
                    name='Tres en Raya', 
                    description='Juego clásico de estrategia para dos jugadores',
                    year=2024,
                    image='https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=300&fit=crop',
                    url='#',
                    user_id=1
                )
            ]
            db.session.add_all(games)
            db.session.commit()
            print(f"✅ {len(games)} juegos creados")
        
        print("🎉 Base de datos inicializada!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
=======
        ]
        db.session.add_all(sample_games)
        db.session.commit()
        print(f"✅ {len(sample_games)} juegos de ejemplo creados")
    
    print("🎉 Base de datos inicializada correctamente!")
>>>>>>> 507a0ad87c99233659851fe5d37325f93c31083c
