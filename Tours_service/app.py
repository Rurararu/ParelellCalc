from flask import Flask, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
import sys
import redis
import json
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import app, db, Customer, Agent, Tour, PaidTour, Discount

api = Api(app)
redis_client = redis.Redis(host='redis', port=6379)

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
        cache_key = "tours:all"
        cached_data = redis_client.get(cache_key)

        if cached_data:
            # app.logger.info("Отримано з Redis")
            time.sleep(2)
            tours = json.loads(cached_data)
            return [Tour(**tour) for tour in tours]

        # app.logger.info("Отримано з БД")
        time.sleep(5)
        tours = Tour.query.all()

        tours_data = []
        for tour in tours:
            tours_data.append({
                'id': tour.id,
                'name': tour.name,
                'description': tour.description,
                'price': tour.price,
                'status': tour.status,
                'agent_id': tour.agent_id
            })

        redis_client.setex(cache_key, 60, json.dumps(tours_data))  
        return tours
    

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