from app.init import create_app, db
from app.models import User, Game
import sqlalchemy as sa

app = create_app()

with app.app_context():
    try:
        # Crear todas las tablas
        db.create_all()
        
        # Verificar tablas creadas (método moderno)
        inspector = sa.inspect(db.engine)
        table_names = inspector.get_table_names()
        print("✅ Tablas creadas en PostgreSQL:", table_names)
        
        # Crear usuario admin por defecto
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@portal.com',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Usuario admin creado: admin / admin123")
        else:
            print("✅ Usuario admin ya existe")
        
        # Agregar juegos de ejemplo si no existen
        if Game.query.count() == 0:
            sample_games = [
                Game(
                    name='The Legend of Zelda: Breath of the Wild',
                    description='Aventura épica en el reino de Hyrule',
                    year=2017,
                    image='https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=300&fit=crop',
                    url='https://zelda.com',
                    user_id=admin_user.id
                ),
                Game(
                    name='Tres en Raya', 
                    description='Juego clásico de estrategia para dos jugadores',
                    year=2024,
                    image='https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&h=300&fit=crop',
                    url='#',
                    user_id=admin_user.id
                )
            ]
            db.session.add_all(sample_games)
            db.session.commit()
            print("✅ Juegos de ejemplo agregados")
        else:
            print(f"✅ Ya existen {Game.query.count()} juegos en la base de datos")
        
        print("🎉 Base de datos PostgreSQL inicializada correctamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Posibles soluciones:")
        print("   1. Verifica que PostgreSQL esté ejecutándose")
        print("   2. Revisa la conexión en .env")
        print("   3. Asegúrate de que la base de datos 'portal_juegos' existe")