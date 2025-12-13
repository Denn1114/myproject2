from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'client'
    __table_args__ = {'extend_existing': True}  # <-- ось це
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

class Order(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}  # <-- теж додати
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    product = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "client_id": self.client_id, "product": self.product}
