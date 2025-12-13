from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from marshmallow import Schema, fields, validate
import os

app = Flask(__name__)
CORS(app)

# ================== DB ==================
db_path = os.path.join(os.path.dirname(__file__), "shop.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ================== Swagger ==================
swagger_config = {
    "headers": [],
    "specs": [{"endpoint": 'apispec', "route": '/apispec.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
Swagger(app, config=swagger_config)

# ================== Models ==================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "stock": self.stock}

# ================== Schema ==================
class ProductSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True)
    stock = fields.Integer(required=True)

product_schema = ProductSchema()

# ================== Error ==================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

# ================== REST API ==================
@app.route('/api/v1/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/v1/products', methods=['POST'])
def create_product():
    errors = product_schema.validate(request.json)
    if errors:
        return jsonify(errors), 400
    data = request.json
    product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

# ================== Web Pages ==================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/shop", methods=["GET", "POST"])
def shop():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock"))
        data = {"name": name, "price": price, "stock": stock}
        response = app.test_client().post("/api/v1/products", json=data)
        if response.status_code == 201:
            message = f"Продукт {name} додано успішно!"
        else:
            message = f"Помилка: {response.json}"

    products = Product.query.all()
    return render_template("shop.html", products=products, message=message)

# ================== Run ==================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
