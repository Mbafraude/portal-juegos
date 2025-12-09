from app.init import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("✅ Usuario 'admin' ahora es administrador")
    else:
        print("❌ Usuario 'admin' no encontrado")