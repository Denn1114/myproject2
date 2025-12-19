Звіт з лабораторної роботи 4
Реалізація бази даних для вебпроєкту
Інформація про команду

Назва команди: WebDev Team

Учасники:

Мазурок Денис (тім-лідер, проєктування БД)

Березовий Арсеній (тестер, реалізація CRUD)

Завдання
Обрана предметна область

Наш вебзастосунок — це інтернет-магазин для фанатів футбольного клубу, де користувачі можуть переглядати каталог товарів, додавати їх до кошика, оформлювати замовлення та залишати відгуки.

Для цього потрібно зберігати такі дані:

Інформація про користувачів (ім’я, email, роль адміністратора).

Товари (назва, опис, ціна, фото).

Замовлення (товари, кількість, користувач, статус).

Відгуки (текст, автор, дата створення).

Реалізовані вимоги

 Рівень 1: Створено базу даних SQLite з таблицями для користувачів, відгуків, товарів та замовлень; реалізовано базові CRUD операції; створено адмін-панель для перегляду відгуків та управління товарами.

 Рівень 2: Додано таблицю клієнтів (Client), реалізовано роботу з клієнтами через адмін-панель.

 Рівень 3: Додано можливість блокування користувачів та видалення відгуків через адмін-панель.

Хід виконання роботи
Підготовка середовища розробки

Версія Python: 3.11

Встановлені бібліотеки: Flask, Flask-Login, Flask-SQLAlchemy, Werkzeug, Flasgger

Інші інструменти: SQLite, Visual Studio Code, Postman для тестування API

Структура проєкту
project/
├── app.py
├── models.py
├── routes/
│   ├── __init__.py
│   ├── admin.py
│   ├── feedback.py
│   └── shop.py
├── templates/
│   ├── base.html
│   ├── admin/
│   ├── feedback/
│   └── shop/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── db.sqlite
└── lab-reports/
    └── lab04-report-student-id.md

Проектування бази даних
Схема бази даних
Таблиця "users":
- id (INTEGER, PRIMARY KEY)
- username (TEXT, NOT NULL)
- password (TEXT, NOT NULL)
- is_admin (BOOLEAN, DEFAULT FALSE)

Таблиця "feedback":
- id (INTEGER, PRIMARY KEY)
- text (TEXT, NOT NULL)

Таблиця "products":
- id (INTEGER, PRIMARY KEY)
- name (TEXT, NOT NULL)
- price (REAL, NOT NULL)
- image (TEXT, NOT NULL)

Таблиця "orders":
- id (INTEGER, PRIMARY KEY)
- description (TEXT, NOT NULL)

Таблиця "clients":
- id (INTEGER, PRIMARY KEY)
- name (TEXT, NOT NULL)
- email (TEXT, NOT NULL)
- phone (TEXT, NOT NULL)

Опис реалізованої функціональності
Система відгуків

Користувачі можуть залишати відгуки через форму на сайті.

Всі відгуки зберігаються у таблиці feedback.

Адміністратор може переглядати та видаляти відгуки через адмін-панель.

Магазин

Відображення каталогу товарів з бази products.

Додавання товарів до кошика та оформлення замовлення (orders).

Управління товарами через адмін-панель (додавання/редагування/видалення).

Адміністративна панель

Перегляд користувачів і блокування облікових записів.

Перегляд відгуків і їх видалення.

Перегляд замовлень (редагування статусу, якщо потрібно).

Додаткова функціональність

Блокування користувачів (is_admin = False не дозволяє доступ до адмін-панелі).

Видалення відгуків через адмін-панель.

Ключові фрагменти коду
Ініціалізація бази даних (models.py)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

CRUD операції

Додавання відгуку:

feedback = Feedback(text="Це тестовий відгук")
db.session.add(feedback)
db.session.commit()


Отримання всіх відгуків:

feedbacks = Feedback.query.all()


Видалення відгуку:

fb = Feedback.query.get(feedback_id)
db.session.delete(fb)
db.session.commit()


Блокування користувача:

user = User.query.get(user_id)
user.is_admin = False
db.session.commit()

Розподіл обов'язків у команді

Мазурок Денис: проектування схеми БД, створення моделей, налаштування зв’язків між таблицями

Березовий Арсеній: реалізація маршрутів, CRUD операцій, адмін-панель, тестування

Скріншоти

Форма зворотного зв'язку:


Каталог товарів:


Адміністративна панель:


Управління замовленнями:


Додаткова функціональність:


Тестування

Додавання нового відгуку та перевірка його відображення в адмін-панелі ✅

Створення товару, додавання до кошика та оформлення замовлення ✅

Зміна статусу замовлення через адмін-панель ✅

Видалення відгуків та блокування користувачів ✅

Перевірка валідації даних при реєстрації та замовленнях ✅

Висновки

Вдалося реалізувати базову базу даних для інтернет-магазину та систему відгуків.

Отримані навички роботи з Flask, SQLAlchemy та SQLite.

Основні труднощі були пов’язані з налаштуванням адмін-панелі та зв’язків між таблицями.

Командна робота була організована за принципом розподілу обов’язків: один розробляв модель та базу даних, інший — маршрути і адмінку.

Можливі покращення: додати авторизацію на рівні ролей, інтегрувати email-повідомлення про нові замовлення та відгуки.