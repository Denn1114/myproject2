# seed.py
from models import db, User, Feedback, Order, Client
from werkzeug.security import generate_password_hash
from app import app

with app.app_context():
    # ------------------------------
    # Тестові користувачі
    # ------------------------------
    if User.query.count() == 0:
        users = [
            User(username="admin", password_hash=generate_password_hash("admin123")),
            User(username="user1", password_hash=generate_password_hash("pass1")),
            User(username="user2", password_hash=generate_password_hash("pass2")),
        ]
        db.session.add_all(users)
        print("Користувачі додані")

    # ------------------------------
    # Тестові відгуки
    # ------------------------------
    if Feedback.query.count() == 0:
        feedbacks = [
            Feedback(text="Це перший тестовий відгук"),
            Feedback(text="Дуже хороший сервіс!"),
            Feedback(text="Замовлення прийшло вчасно"),
        ]
        db.session.add_all(feedbacks)
        print("Відгуки додані")

    # ------------------------------
    # Тестові замовлення
    # ------------------------------
    if Order.query.count() == 0:
        orders = [
            Order(description="Товар A x 2"),
            Order(description="Товар B x 1"),
            Order(description="Товар C x 5"),
        ]
        db.session.add_all(orders)
        print("Замовлення додані")

    # ------------------------------
    # Тестові клієнти (для адмінки)
    # ------------------------------
    if Client.query.count() == 0:
        clients = [
            Client(name="Іван Іванов", email="ivan@example.com", phone="+380123456789"),
            Client(name="Петро Петренко", email="petro@example.com", phone="+380987654321"),
        ]
        db.session.add_all(clients)
        print("Клієнти додані")

    db.session.commit()
    print("Сидинг бази завершено!")
