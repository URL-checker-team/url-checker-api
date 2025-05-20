from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            password=generate_password_hash('123456')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
    else:
        print("⚠️ Admin user already exists")
