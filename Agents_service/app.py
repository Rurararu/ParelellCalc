from flask import Flask, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import app, db, Customer, Agent, Tour, PaidTour, Discount

api = Api(app)

agent_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'number': fields.String,
    'region': fields.String
}

discount_fields = {
    'id': fields.Integer,
    'customer_id': fields.Integer,
    'agent_id': fields.Integer,
    'discount': fields.Float
}

class Agents(Resource):
    
    @marshal_with(agent_fields)
    def get(self):
        return Agent.query.all()
    
    @marshal_with(agent_fields)
    def post(self):
        data = request.json
        agent = Agent(name=data['name'], email=data['email'], number=data['number'], region=data['region'])
        db.session.add(agent)
        db.session.commit()
        return agent, 201
    
class AgentResource(Resource):
    
    @marshal_with(agent_fields)
    def get(self, agent_id):
        return Agent.query.get_or_404(agent_id)

class Disounts(Resource):
    
    @marshal_with(discount_fields)
    def get(self):
        return Discount.query.all()
    
class DiscountAgentResource(Resource):
    
    @marshal_with(discount_fields)
    def post(self, agent_id):
        data = request.json
        discount = Discount(customer_id=data['customer_id'], agent_id=agent_id, discount=data['discount'])
        db.session.add(discount)
        db.session.commit()
        return discount, 201
    
class DisountsCustomer(Resource):
    
    @marshal_with(discount_fields)
    def get(self, customer_id):
        return Discount.query.filter_by(customer_id=customer_id).all()

api.add_resource(Agents, '/api/agents/')    
api.add_resource(AgentResource, '/api/agent/<int:agent_id>')


api.add_resource(Disounts, '/api/discounts/')
api.add_resource(DisountsCustomer, '/api/discounts/<int:customer_id>')
api.add_resource(DiscountAgentResource, '/api/agent/<int:agent_id>/discounts/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)