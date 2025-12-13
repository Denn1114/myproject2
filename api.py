from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from models import db, Client, Order
from marshmallow import Schema, fields, validate

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

swagger_config = {
    "headers": [],
    "specs": [{"endpoint": 'apispec', "route": '/apispec.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
Swagger(app, config=swagger_config)

# ================= Schemas =================
class ClientSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email()

class OrderSchema(Schema):
    client_id = fields.Integer(required=True)
    product = fields.String(required=True, validate=validate.Length(min=1))

client_schema = ClientSchema()
order_schema = OrderSchema()

# ================= Error Handlers =================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

# ================= CLIENTS =================
@app.route('/api/v1/clients', methods=['GET'])
def get_clients_v1():
    """
    Get list of clients
    ---
    responses:
      200:
        description: List of clients
    """
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients])

@app.route('/api/v1/clients/<int:id>', methods=['GET'])
def get_client_v1(id):
    """
    Get a client by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200: Client found
      404: Client not found
    """
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(client.to_dict())

@app.route('/api/v1/clients', methods=['POST'])
def create_client_v1():
    """
    Create a new client
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema: ClientSchema
    responses:
      201: Client created
      400: Validation errors
    """
    errors = client_schema.validate(request.json)
    if errors:
        return jsonify(errors), 400
    data = request.json
    client = Client(name=data['name'], email=data.get('email'))
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

# ================= ORDERS =================
@app.route('/api/v1/orders', methods=['GET'])
def get_orders_v1():
    """Get list of orders"""
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

@app.route('/api/v1/orders/<int:id>', methods=['GET'])
def get_order_v1(id):
    """Get an order by ID"""
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.to_dict())

@app.route('/api/v1/orders', methods=['POST'])
def create_order_v1():
    """Create a new order"""
    errors = order_schema.validate(request.json)
    if errors:
        return jsonify(errors), 400
    data = request.json
    order = Order(client_id=data['client_id'], product=data['product'])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
