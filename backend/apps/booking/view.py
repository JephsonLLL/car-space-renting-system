from flask import Flask, request, Blueprint,jsonify 
import json
import os, sys 
from database.session import get_session 
from database.dbTables import CarSpaceReview, UserBankDetails, CarSpace, CarSpaceTags, Bookings 
from backend.utils import db_object_to_dict 
from booking.bookings import make_booking, cancel_booking, get_bookings
from flask_jwt_extended import decode_token
import datetime

from copy import deepcopy 

booking_bp = Blueprint('booking', __name__) 
@booking_bp.route('/api/make_booking', methods=['POST']) 
def make_a_booking(): 
    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    consumer_id = token["sub"]["id"]

    car_space_id = request.json['id'] 
    # consumer_id = request.json['consumer_id'] 
    #start_date = request.json['start_date'] 
    #end_date = request.json['end_date'] 

    time = request.json['bookdate']

    start_date = datetime.date.fromisoformat(time[0].split('T')[0])
    end_date = datetime.date.fromisoformat(time[1].split('T')[0])


    distance = 4
    #distance = request.json['distance'] 
    
    # if not (car_space_id and consumer_id and start_date and end_date):
    #     return jsonify({'msg': "All fields are required!"}), 400 
    
    res, msg, status = make_booking(car_space_id=car_space_id, 
                                    consumer_id=consumer_id, 
                                    start_date=start_date, 
                                    end_date=end_date, distance=distance) 
    
    return jsonify({'msg': msg}), status 

@booking_bp.route('/api/cancel_booking', methods=['POST'])
def cancel_a_booking(): 
    data = request.get_json()  
    booking_id = data['booking_id'] 
    
    res, msg, status = cancel_booking(booking_id) 
    
    return jsonify({'msg': msg}), status 

@booking_bp.route('/api/view_my_bookings', methods=['GET'])
def view_my_bookings():
   headers = request.headers
   authorization = headers['Authorization']
   token = decode_token(authorization)
   user= token["sub"]["id"]
   # provider = request.args.get('provider_id')
   list_c = get_bookings(user)
   for car_space in list_c:
      car_space['start_date'] = car_space['start_date'].strftime('%Y-%m-%d')
      car_space['end_date'] = car_space['end_date'].strftime('%Y-%m-%d')

   json_data = json.dumps(list_c)

   return json_data
