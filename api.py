from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Feedback, Order, Client

api = Blueprint("api", __name__, url_prefix="/api")

# ===== AUTH =====
@api.route("/register", methods=["POST"])
def register():
    """
    Реєстрація користувача
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Користувач зареєстрований
    """
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User exists"}), 400
    user = User(username=data["username"], password_hash=generate_password_hash(data["password"]))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully"})


@api.route("/login", methods=["POST"])
def login():
    """
    Логін
    ---
    tags:
      - Auth
    """
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Login success"})
    return jsonify({"error": "Invalid credentials"}), 401

# ===== FEEDBACK =====
@api.route("/feedback/list", methods=["GET"])
def feedback_list():
    """
    Список відгуків
    ---
    tags:
      - Feedback
    """
    feedbacks = Feedback.query.all()
    return jsonify([{"id": f.id, "text": f.text} for f in feedbacks])

@api.route("/feedback/add", methods=["POST"])
def feedback_add():
    """
    Додати відгук
    ---
    tags:
      - Feedback
    """
    data = request.json
    feedback = Feedback(text=data["text"])
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback added"})


# ===== ORDERS =====
@api.route("/orders/my", methods=["GET"])
def my_orders():
    """
    Мої замовлення
    ---
    tags:
      - Orders
    """
    orders = Order.query.all()
    return jsonify([{"id": o.id, "description": o.description} for o in orders])

@api.route("/orders/add", methods=["POST"])
def order_add():
    """
    Додати замовлення
    ---
    tags:
      - Orders
    """
    data = request.json
    order = Order(description=data["description"])
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order added"})


# ===== CLIENTS (ADMIN) =====
@api.route("/admin/clients", methods=["GET"])
def admin_clients():
    """
    Клієнти (адмін)
    ---
    tags:
      - Admin
    """
    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone} for c in clients])
