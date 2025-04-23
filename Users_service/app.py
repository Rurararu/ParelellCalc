from flask import Flask, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import app, db, Customer, Agent, Tour, PaidTour, Discount

api = Api(app)

customer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'number': fields.String, 
    'password':fields.String
}

class Customers(Resource):
    
    @marshal_with(customer_fields)
    def get(self):
        return Customer.query.all()
    
    @marshal_with(customer_fields)
    def post(self):
        data = request.json
        customer = Customer(name=data['name'], email=data['email'], number=data['number'], password=data['password'])
        db.session.add(customer)
        db.session.commit()
        return customer, 201
    
class CustomerResource(Resource):
    
    @marshal_with(customer_fields)
    def get(self, customer_id):
        return Customer.query.get_or_404(customer_id)
    

api.add_resource(Customers, '/api/customers/')    
api.add_resource(CustomerResource, '/api/customer/<int:customer_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)