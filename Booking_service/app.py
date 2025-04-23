from flask import Flask, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import app, db, Customer, Agent, Tour, PaidTour, Discount
import requests

api = Api(app)

TOURS_SERVICE_URL = "http://tours_service:5003/api/tours/"
AGENTS_SERVICE_URL = "http://agents_service:5002/api/discounts/"

paid_tour_fields = {
    'id': fields.Integer,
    'tour_id': fields.Integer,
    'customer_id': fields.Integer,
    'start_date': fields.String,
    'end_date': fields.String,
    'price': fields.Float
}

class PaidTours(Resource):
    
    @marshal_with(paid_tour_fields)
    def get(self, customer_id):
        return PaidTour.query.filter_by(customer_id=customer_id).all()
    
    @marshal_with(paid_tour_fields)
    def post(self, customer_id):
        data = request.json
        tour_id = data['tour_id']

        tour_response = requests.get(f"{TOURS_SERVICE_URL}{tour_id}")
        if tour_response.status_code != 200:
            return {"error": "Tour not found"}, 404

        tour_data = tour_response.json()
        # print("TOUR DATA:", tour_data)

        final_price = tour_data.get('price')
        if final_price is None:
            return {"error": "Tour price not found"}, 500

        discount_response = requests.get(f"{AGENTS_SERVICE_URL}{customer_id}")
        if discount_response.status_code != 200:
            return {"error": "Discount not found"}, 404

        discount_data = discount_response.json()
        # print("DISCOUNT DATA:", discount_data)

        if isinstance(discount_data, list) and len(discount_data) > 0:
            discount = discount_data[0]
            if 'discount' in discount:
                final_price *= (1 - discount['discount'] / 100.0)

        paid_tour = PaidTour(
            tour_id=tour_id,
            customer_id=customer_id,
            start_date=data['start_date'],
            end_date=data['end_date'],
            price=final_price
        ) 
        db.session.add(paid_tour)
        db.session.commit() 
        return paid_tour, 201
    
class PaidToursResource(Resource):
    
    @marshal_with(paid_tour_fields)
    def get(self):
        return PaidTour.query.all()

api.add_resource(PaidTours, '/api/customer/<int:customer_id>/paid_tours/')

api.add_resource(PaidToursResource, '/api/paid_tours/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)