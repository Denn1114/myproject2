from app import app
from models import db, User, Product
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Створюємо адміна
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=generate_password_hash("050909"), is_admin=True)
        db.session.add(admin)

    db.session.commit()
    print("База створена і таблиці заповнені!")
