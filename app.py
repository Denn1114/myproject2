from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger
from models import db, User, Feedback, Order, Client, Product
from api import api  # ваш api.py
from functools import wraps
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Доступ заборонено!")
            return redirect(url_for("login.html"))
        return f(*args, **kwargs)
    return decorated_function
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ================= CONFIG =================
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ================= INIT =================
db.init_app(app)
app.register_blueprint(api)
Swagger(app)

# ================= CREATE DB =================
with app.app_context():
    db.create_all()


# ================= ROUTES =================




@app.route("/admin")
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Доступ заборонено!")
        return redirect(url_for("index"))
    
    users = User.query.all()
    orders = Order.query.all()
    feedbacks = Feedback.query.all()
    
    return render_template(
        "admin.html",
        users=users,
        orders=orders,
        feedbacks=feedbacks
    )


@app.route("/admin/clients")
@admin_required
def admin_clients():
    # приклад: отримати всіх користувачів
    from models import User
    users = User.query.all()
    return render_template("admin_clients.html", users=users)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/contacts")
def contacts_page():
    return render_template("contacts.html")

# ================= CATALOG =================
@app.route("/catalog")
def catalog_page():
    products = Product.query.all()
    return render_template("catalog.html", products=products)

# ================= ORDERS =================
@app.route("/my_orders")
def my_orders_page():
    orders = Order.query.all()
    return render_template("my_orders.html", orders=orders)

@app.route("/order/add", methods=["GET", "POST"])
def order_add_page():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        quantity = request.form.get("quantity")
        order = Order(description=f"{product_name} x {quantity}")
        db.session.add(order)
        db.session.commit()
        flash("Замовлення додано!", "success")
        return redirect(url_for("my_orders_page"))
    return render_template("order_add.html")

# ================= FEEDBACK =================
@app.route("/feedback")
def feedback_list_page():
    feedbacks = Feedback.query.all()
    return render_template("feedback_list.html", feedbacks=feedbacks)

@app.route("/feedback/add", methods=["GET", "POST"])
def feedback_add_page():
    if request.method == "POST":
        text = request.form.get("text")
        feedback = Feedback(text=text)
        db.session.add(feedback)
        db.session.commit()
        flash("Відгук додано!", "success")
        return redirect(url_for("feedback_list_page"))
    return render_template("feedback_add.html")

# ================= AUTH =================
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            flash("Користувач вже існує", "danger")
            return redirect(url_for("register_page"))
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Реєстрація успішна!", "success")
        return redirect(url_for("login_page"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Успішний вхід!", "success")
            return redirect(url_for("index"))
        else:
            flash("Невірний логін або пароль", "danger")
            return redirect(url_for("login_page"))

    return render_template("login.html")

@app.route("/logout")
def logout_page():
    session.pop("user_id", None)
    flash("Ви вийшли з акаунту", "info")
    return redirect(url_for("login_page"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)