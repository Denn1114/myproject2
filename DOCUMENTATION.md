# Документація проєкту MyProject

## 1. Опис проєкту
MyProject — веб-застосунок на Flask з підтримкою користувачів, замовлень, відгуків і адмін-панелі.  
Застосунок контейнеризований через Docker для легкого розгортання.

---

## 2. Архітектура проєкту
myproject/
│
├── app.py # Основний Flask застосунок
├── models.py # SQLAlchemy моделі (User, Order, Product, Feedback, Client)
├── api.py # REST API Blueprint
├── templates/ # HTML-шаблони
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── admin.html
│ ├── admin_order_add.html
│ └── ...
├── static/ # CSS, JS, картинки
├── Dockerfile # Dockerfile для контейнеризації
├── docker-compose.yml # Docker Compose конфігурація
├── requirements.txt # Python dependencies
└── .env # Змінні середовища (секретні ключі, база)


---

## 3. Використані технології
- **Python 3.11+**  
- **Flask** – веб-фреймворк  
- **Flask-Login** – авторизація/аутентифікація  
- **Flask-SQLAlchemy** – ORM для SQLite  
- **Werkzeug** – хешування паролів  
- **Flasgger** – документація API  
- **SQLite** – файловa база даних  
- **Docker & Docker Compose** – контейнеризація  
- **Bootstrap 5** – фронтенд  

---

## 4. Структура бази даних

| Модель | Поля |
|--------|------|
| User | id, username, password, is_admin |
| Product | id, name, price, image |
| Order | id, description, client_name |
| Feedback | id, text |
| Client | id, name, email |

---

## 5. Інструкції користувача

### 5.1 Реєстрація та вхід
1. Відкрити `/register` → створити акаунт  
2. Відкрити `/login` → увійти під своїм акаунтом  
3. Якщо `is_admin=True` → доступна адмін-панель `/admin`  

### 5.2 Адмін-панель
- `/admin` – перегляд користувачів, замовлень та відгуків  
- `/admin/orders/add` – додати замовлення  
- `/admin/clients` – список клієнтів  

### 5.3 Робота зі звичайним користувачем
- `/catalog` – перегляд товарів  
- `/my_orders` – власні замовлення  
- `/order/add` – додати замовлення  
- `/feedback` – перегляд відгуків  
- `/feedback/add` – додати відгук  