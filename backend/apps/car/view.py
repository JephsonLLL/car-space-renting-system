from flask import Flask, request, Blueprint,jsonify
car_bp = Blueprint('register_car_space', __name__)
from backend.carspace import register_new_car_space, update_car_space, delete_car_space, get_provider_car_spaces, recommend_price_carspace
from backend.login_backend import get_user_profile_by_id
import datetime
from flask_jwt_extended import decode_token
import json


@car_bp.route('/api/view_my_car_spaces', methods=['GET'])
def view_my_car_spaces():
   headers = request.headers
   authorization = headers['Authorization']
   token = decode_token(authorization)
   provider= token["sub"]["id"]
   # provider = request.args.get('provider_id')
   list_c = get_provider_car_spaces(provider)
   for car_space in list_c:
      car_space['available_start_date'] = car_space['available_start_date'].strftime('%Y-%m-%d')
      car_space['available_end_date'] = car_space['available_end_date'].strftime('%Y-%m-%d')

   json_data = json.dumps(list_c)

   return json_data



@car_bp.route('/api/register_car_space', methods=['POST'])
def register_car_space():
   #car_space_name = request.form['car_space_name']
   #daily_cost = request.form["daily_cost"]
   #provider = 1
   
   address = request.json["address"]
   lat = request.json["lat"]
   lng = request.json["lng"]
   
   length = request.json["spaceLength"]
   width = request.json["spaceWidth"]

   time = request.json['availableDate']
   price = request.json["price"]

   start_date = datetime.date.fromisoformat(time[0].split('T')[0])
   end_date = datetime.date.fromisoformat(time[1].split('T')[0])

   headers = request.headers
   authorization = headers['Authorization']
   token = decode_token(authorization)
   provider= token["sub"]["id"]


   is_succuss, message, code = register_new_car_space(provider=provider, 
                                                      address=address,
                                                      lat=lat,
                                                      lng=lng,
                                                      length=length, 
                                                      width=width,
                                                      price=price, 
                                                      auto_price=False, 
                                                      available_start_date=start_date,
                                                      available_end_date=end_date)
   
   return jsonify({"msg": message}), code 

@car_bp.route('/api/update_car_space', methods=['POST'])
def update_carspace():
   # headers = request.headers
   # authorization = headers['Authorization']
   # token = decode_token(authorization)
   # provider= token["sub"]["id"]

   # get car space id here 
   id = request.json["car_space_id"]

   address = request.json["address"]
   lat = request.json["lat"]
   lng = request.json["lng"]
   
   length = request.json["spaceLength"]
   width = request.json["spaceWidth"]

   time = request.json['availableDate']
   price = request.json["price"]

   start_date = datetime.date.fromisoformat(time[0].split('T')[0])
   end_date = datetime.date.fromisoformat(time[1].split('T')[0])

   update_car_space(id, address,lat,lng,length,width,price,start_date,end_date)


   return jsonify({"msg": "success"}) 




@car_bp.route('/api/delete_car_space', methods=['POST'])
def delte_carspace():
   # get car space id here 
   id = request.json["car_space_id"]

   delete_car_space(id)

   return jsonify({"msg": "success"}) 


@car_bp.route('/api/recommendPrice', methods=['POST'])
def recommend_price_per_day():
   lat = request.json["lat"]
   lng = request.json["lng"]

   length = request.json["spaceLength"]
   width = request.json["spaceWidth"]

   ret = recommend_price_carspace(lat,lng, length, width)

   return ret, 200
