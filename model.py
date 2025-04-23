from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tourist_agency.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    paid_tours = db.relationship('PaidTour', backref='customer', lazy=True)
    personal_discount = db.relationship('Discount', backref='customer', lazy=True)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    number = db.Column(db.String(20), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    tours = db.relationship('Tour', backref='agent', lazy=True)
    discounts = db.relationship('Discount', backref='agent', lazy=True)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    paid_tours = db.relationship('PaidTour', backref='tour', lazy=True)

class PaidTour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    discount = db.Column(db.Float, nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("DB was created!")
