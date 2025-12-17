from app import app, db
from models import Product, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin / admin123")
products = [
        Product(name="Футболка Барселона 2025", price=79.99, image="jersey1.jpg"),
        Product(name="Шарф Барселона", price=29.99, image="scarf1.jpg"),
        Product(name="Кепка Барселона", price=24.99, image="cap1.jpg")
    ]
db.session.add_all(products)
db.session.commit()

print("База shop.db створена і таблиці заповнені товарами!")