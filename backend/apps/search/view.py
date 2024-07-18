from flask import Flask, request, jsonify, Blueprint 
from flask_jwt_extended import decode_token
import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
from search.car_space_recommnedation_system import * 
from backend.utils import * 
from search.sort_car_spaces import sort_car_spaces 
from search.bookmark import get_bookmarked_carspaces

search_bp = Blueprint('search', __name__)
@search_bp.route('/api/search', methods=['POST'])
def search_car_parks():
    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    consumer_id= token["sub"]["id"]

    # consumer_id = request.args.get('consumer_id')

    # current_address = request.json['currentAddress'] # lat, lon 
    lat = request.json['lat']
    lon = request.json['lon']
    distance = request.json['distance']  # within 
    start_date = request.json['startDate'] 
    end_date = request.json['endDate']
    sort_by = request.json['sort_by'] # "distance", "price", "rating", default is recommendation 


    ## get car spaces with in distance 
    # lat, lon = get_lat_lon_for_address(address=current_address) 
    filtered_car_spaces = find_car_spaces_within_distance(consumer_id=consumer_id, 
                                                          lat=lat, lon=lon, distance=distance) 
    ## filer car spaces by available dates 
    filtered_car_spaces = get_available_car_space(start_date=start_date, 
                                                  end_date=end_date, 
                                                  car_space_list=filtered_car_spaces) 
    

    if sort_by == ("distance" or "price" or "rating"):
        ## if not using the car space recommendation system, just sort it 

        res = sort_car_spaces(filtered_car_spaces, sort_by)
        for car_space in res:
            car_space['available_start_date'] = car_space['available_start_date'].strftime('%Y-%m-%d')
            car_space['available_end_date'] = car_space['available_end_date'].strftime('%Y-%m-%d')

        res = json.dumps(res)
    else:

        ## if want to use car space recommendation system 
        sorted_car_spaces = main_car_space_recommendation(user_id=consumer_id, 
                                                          filtered_car_spaces=filtered_car_spaces)
        res = json.dumps(sorted_car_spaces) 

    return jsonify(res)

@search_bp.route('/api/bookmarked', methods=['POST'])
def display_bookmarked_carspaces():
    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    consumer_id= token["sub"]["id"]

    sort_by = request.json['sort_by'] # "distance", "price", "rating", default is recommendation 

    # unlike search, this query does not filter carspaces by distance or availability time

    filtered_car_spaces = get_bookmarked_carspaces(user_id=consumer_id)

    if sort_by == ("distance" or "price" or "rating"):
        ## if not using the car space recommendation system, just sort it 

        res = sort_car_spaces(filtered_car_spaces, sort_by)
        for car_space in res:
            car_space['available_start_date'] = car_space['available_start_date'].strftime('%Y-%m-%d')
            car_space['available_end_date'] = car_space['available_end_date'].strftime('%Y-%m-%d')

        res = json.dumps(res)
    else:

        ## if want to use car space recommendation system 
        sorted_car_spaces = main_car_space_recommendation(user_id=consumer_id, 
                                                          filtered_car_spaces=filtered_car_spaces)
        res = json.dumps(sorted_car_spaces) 

    return jsonify(res)