from app import app
from models import db, User, Product
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Додаємо приклади продуктів
    products = [
        Product(name="Футболка Барселона 2025", price=79.99, image="jersey1.jpg"),
        Product(name="Шарф Барселона", price=29.99, image="scarf1.jpg"),
        Product(name="Кепка Барселона", price=24.99, image="cap1.jpg")
    ]
    db.session.add_all(products)

    # Створюємо адміна
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=generate_password_hash("050909"), is_admin=True)
        db.session.add(admin)

    db.session.commit()
    print("База створена і таблиці заповнені!")
