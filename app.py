from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# --- Моделі ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_name = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Шаблони як рядки (щоб нічого не пропало) ---
home_template = '''
<h1>Фан-шоп Барселони</h1>
{% if current_user.is_authenticated %}
<p>Ласкаво просимо, {{ current_user.username }}!</p>
<a href="{{ url_for('catalog') }}">Каталог</a> | 
<a href="{{ url_for('orders') }}">Мої замовлення</a> | 
<a href="{{ url_for('logout') }}">Вийти</a>
{% else %}
<a href="{{ url_for('register') }}">Реєстрація</a> | 
<a href="{{ url_for('login') }}">Логін</a>
{% endif %}
'''

catalog_template = '''
<h2>Каталог товарів</h2>
<ul>
<li>Футболка Барселони</li>
<li>Шарф Барселони</li>
<li>Кепка Барселони</li>
</ul>
<a href="{{ url_for('home') }}">На головну</a>
'''

# --- Основні сторінки ---
@app.route("/")
def home():
    return render_template_string(home_template)

@app.route("/catalog")
@login_required
def catalog():
    return render_template_string(catalog_template)

# --- Реєстрація ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            return "Користувач вже існує"
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("home"))
    return '''
        <h2>Реєстрація</h2>
        <form method="post">
        Логін: <input type="text" name="username"><br>
        Пароль: <input type="password" name="password"><br>
        <input type="submit" value="Зареєструватися">
        </form>
    '''

# --- Логін ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        return "Неправильний логін або пароль"
    return '''
        <h2>Логін</h2>
        <form method="post">
        Логін: <input type="text" name="username"><br>
        Пароль: <input type="password" name="password"><br>
        <input type="submit" value="Увійти">
        </form>
    '''

# --- Логаут ---
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# --- Мої замовлення ---
@app.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders_list = "<ul>"
    for o in orders:
        orders_list += f"<li>{o.item_name}</li>"
    orders_list += "</ul>"
    return f"<h2>Мої замовлення</h2>{orders_list}" \
           f"<a href='/add_order'>Додати замовлення</a> | <a href='/logout'>Вийти</a>"

# --- Додати замовлення ---
@app.route("/add_order", methods=["GET", "POST"])
@login_required
def add_order():
    if request.method == "POST":
        item_name = request.form["item_name"]
        order = Order(user_id=current_user.id, item_name=item_name)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("orders"))
    return '''
        <h2>Додати замовлення</h2>
        <form method="post">
        Назва товару: <input type="text" name="item_name"><br>
        <input type="submit" value="Додати">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)