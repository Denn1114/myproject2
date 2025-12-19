import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger
from models import CartItem, db, User, Feedback, Order, Client, Product
from api import api 
from functools import wraps
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "static/uploads"
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
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# ================= INIT =================
db.init_app(app)
app.register_blueprint(api)
Swagger(app)

# ================= CREATE DB =================
with app.app_context():
    db.create_all()
with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin_user = User(
            username="admin",
            password=generate_password_hash("050909"),
            is_admin=True 
        )
        db.session.add(admin_user)
        db.session.commit()

# ================= ROUTES =================

@app.route("/admin/products/add", methods=["GET", "POST"])
@login_required
def admin_product_add():
    if not current_user.is_admin:
        flash("Доступ заборонено")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        product = Product(
            name=name,
            price=float(price),
            description=description
        )
        db.session.add(product)
        db.session.commit()

        flash("Товар додано!", "success")
        return redirect(url_for("catalog_page"))

    return render_template("admin_product_add.html")


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
def admin_client():
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
@login_required
def catalog_page():
    products = Product.query.all()
    return render_template("catalog.html", products=products)

@app.route("/admin/products", methods=["GET", "POST"])
@admin_required
def admin_products():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        image_file = request.files["image"]

        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        product = Product(
            name=name,
            price=price,
            quantity=quantity,
            image=filename
        )
        db.session.add(product)
        db.session.commit()
        flash("Товар додано", "success")

    products = Product.query.all()
    return render_template("admin_products.html", products=products)

@app.route("/admin/products/delete/<int:product_id>")
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Товар видалено", "info")
    return redirect(url_for("admin_products"))

from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'  # директорія для фото
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/admin/products/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_product_add_new():  # <-- змінили ім'я
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity", 0))

        file = request.files.get("image")
        image_path = None
        if file and file.filename != "":
            image_path = f"static/images/{file.filename}"
            file.save(image_path)

        product = Product(
            name=name,
            price=price,
            quantity=quantity,
            image=image_path
        )
        db.session.add(product)
        db.session.commit()
        flash("Товар додано!", "success")
        return redirect(url_for("admin_panel"))

    return render_template("admin_product_add.html")



@app.route("/cart")
@login_required
def cart_page():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(i.product.price * i.quantity for i in items)
    return render_template("cart.html", items=items, total=total)\
    
@app.route("/cart/add/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # Перевіримо, чи користувач вже має кошик (імітований)
    if not hasattr(current_user, "cart"):
        current_user.cart = []

    current_user.cart.append({
        "product_id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": 1
    })
    flash(f"Товар {product.name} додано в кошик", "success")
    return redirect(url_for("catalog_page"))

# ================= ORDERS =================
@app.route("/my_orders")
def my_orders_page():
    orders = Order.query.all()
    return render_template("my_orders.html", orders=orders)

@app.route("/order/add/<int:product_id>", methods=["POST"])
def order_add_from_catalog(product_id):
    product = Product.query.get_or_404(product_id)

    order = Order(
        description=f"{product.name} - {product.price} грн"
    )

    db.session.add(order)
    db.session.commit()

    flash("Товар додано в кошик!", "success")
    return redirect(url_for("my_orders_page"))

@app.route("/checkout")
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(i.product.price * i.quantity for i in items)

    order = Order(user_id=current_user.id, total_price=total)
    db.session.add(order)

    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    flash("Замовлення оформлено!", "success")
    return redirect(url_for("index"))

@app.route("/admin/orders")
@admin_required
def admin_orders():
    orders = Order.query.all()
    return render_template("admin_orders.html", orders=orders)


@app.route("/admin/orders/delete/<int:order_id>")
@admin_required
def admin_delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash("Замовлення видалено", "info")
    return redirect(url_for("admin_orders"))
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