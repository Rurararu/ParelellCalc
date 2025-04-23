from flask import Flask, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import app, db, Customer, Agent, Tour, PaidTour, Discount

api = Api(app)

tour_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'status': fields.Boolean,
    'agent_id': fields.Integer
}

class TourAgentResource(Resource):

    @marshal_with(tour_fields)
    def get(self, agent_id):
        return Tour.query.filter_by(agent_id=agent_id).all()
    
    
    @marshal_with(tour_fields)
    def post(self, agent_id):
        data = request.json
        status = data.get('status', False)
        tour = Tour(name=data['name'], description=data['description'], price=data['price'], agent_id=agent_id, status=status)
        db.session.add(tour)
        db.session.commit()
        return tour, 201
    
    @marshal_with(tour_fields)
    def put(self, agent_id):
        data = request.json
        tour = Tour.query.get_or_404(data['tour_id'])
        tour.name = data['name']
        tour.description = data['description']
        tour.price = data['price']
        tour.status = data['status']
        tour.agent_id = agent_id
        db.session.commit()
        return tour
    
    
class Tours(Resource):
    
    @marshal_with(tour_fields)
    def get(self):
        return Tour.query.all()
    

class ToursResource(Resource):
    
    def delete(self, tour_id):
        tour = Tour.query.get_or_404(tour_id)
        db.session.delete(tour)
        db.session.commit()
        return {'message': 'Tour deleted'}, 200
    
    @marshal_with(tour_fields)
    def get(self, tour_id):
        return Tour.query.get_or_404(tour_id)
   
api.add_resource(TourAgentResource, '/api/agent/<int:agent_id>/tours/')
api.add_resource(Tours, '/api/tours/')
api.add_resource(ToursResource, '/api/tours/<int:tour_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)