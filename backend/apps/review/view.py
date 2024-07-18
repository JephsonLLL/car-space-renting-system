from flask import Flask, request, Blueprint,jsonify 
import os, sys, json
from flask_jwt_extended import decode_token
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
from database.session import get_session 
from database.dbTables import CarSpaceReview, UserBankDetails, CarSpace, CarSpaceTags, Bookings 
from backend.utils import db_object_to_dict 
from copy import deepcopy 


write_review_bp = Blueprint('submit_review', __name__)
## frontend page for submitting reviews 
@write_review_bp.route('/api/submit_review', methods=['POST'])
def submit_review():
    data = request.get_json()

    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    user_id = token["sub"]["id"]

    booking_id = data['booking_id']
    rating = data['rating']
    comment = data.get('comment', None)
    tag_not_clean = int(data.get('tag_not_clean', None))
    tag_not_large_enough = int(data.get('tag_not_large_enough', None))
    tag_not_convenient = int(data.get('tag_not_convenient', None))
    tag_low_quality_price_ratio = int(data.get('tag_low_quality_price_ratio', None))
    tag_very_clean = int(data.get('tag_very_clean', None))
    tag_very_large = int(data.get('tag_very_large', None))
    tag_very_convenient = int(data.get('tag_very_convenient', None))
    tag_high_quality_price_ratio = int(data.get('tag_high_quality_price_ratio', None))

    session = get_session() 
    ## get the booking 
    booking = session.query(Bookings).filter_by(id=booking_id).first() 
    car_space = session.query(CarSpace).filter_by(id=booking.car_space_id).first() 
    new_review = CarSpaceReview(consumer_id=user_id, booking_id=booking_id, 
                                provider_id=car_space.provider_id, 
                                car_space_id=booking.car_space_id,
                                rating=rating, comment=comment,
                                tag_not_clean=tag_not_clean, tag_not_large_enough=tag_not_large_enough,
                                tag_not_convenient=tag_not_convenient, tag_low_quality_price_ratio=tag_low_quality_price_ratio,
                                tag_very_clean=tag_very_clean, tag_very_large=tag_very_large,
                                tag_very_convenient=tag_very_convenient, tag_high_quality_price_ratio=tag_high_quality_price_ratio) 
    
    session.add(new_review) 
    session.commit() 
    
    ## give the provider reward points for having a good rating 
    if new_review.rating >= 4: 
        provider_bank_details = session.query(UserBankDetails).filter_by(user_id=new_review.provider_id).first() 
        if new_review.rating == 5:
            provider_bank_details.balance += 2 
        else: 
            provider_bank_details.balance += 1 

        # if provider_bank_details.reward_points > 10: 
        #     extra_balence = provider_bank_details.reward_points % 10
        #     provider_bank_details.balence += extra_balence 
        #     provider_bank_details.reward_points -= extra_balence * 10 
    
    ## give the consumer reward points for making reviews 
    consumer_bank_details = session.query(UserBankDetails).filter_by(user_id=user_id).first() 
    ## one point for giving a rating 
    if rating is not None:
        consumer_bank_details.reward_points += 0.5
    ## one point for giving a comment and two points for giving a longer comment 
    if comment is not None: 
        # if len(comment) > 5: 
        consumer_bank_details.reward_points += 0.5 
        # elif len(comment) > 20: 
        #     consumer_bank_details.reward_points += 2 
    ## two points for choosing tags 
    if (tag_not_clean or tag_not_large_enough or tag_not_convenient or tag_low_quality_price_ratio or 
        tag_very_clean or tag_very_large or tag_very_convenient or tag_high_quality_price_ratio) is not None: 
        consumer_bank_details.reward_points += 0.5 
    
    ## update car space information 
    car_space_tags = session.query(CarSpaceTags).filter_by(car_space_id=new_review.car_space_id).first() 
    if not car_space_tags: 
        car_space_tags = CarSpaceTags(car_space_id=new_review.car_space_id) 
        session.add(car_space_tags) 
    ## update rating 
    car_space_tags.update_rating(new_review=new_review) 
    session.commit() 
    ## update the average rating of the car space
    car_space = session.query(CarSpace).filter_by(id=new_review.car_space_id).first() 
    ## get the updated tags
    car_space_tags = session.query(CarSpaceTags).filter_by(car_space_id=new_review.car_space_id).first()
    car_space.rating = car_space_tags.get_average_rating() 
    ## update tags 
    car_space.tags = car_space_tags.top_N_tags(N=3) 
    session.commit() 
    session.close() 

    return jsonify({'message': 'Review submitted successfully!'}), 200 

@write_review_bp.route('/api/get_review', methods=['GET'])
def get_review():
    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    user= token["sub"]["id"]
    car_space_id = request.json['car_space_id']
    session = get_session() 
    reviews = session.query(CarSpaceReview).filter_by(car_space_id=car_space_id).all()  

    review_list = []
    for r in reviews:
        r_todict = {key: value for key, value in r.__dict__.items() if not key.startswith('_')}
        review_list.append(r_todict)
    for rr in review_list:
        rr['timestamp'] = rr['timestamp'].strftime('%Y-%m-%d')

    json_data = json.dumps(review_list)
    return json_data



review_bp = Blueprint('car_park_reviews', __name__)
@review_bp.route('/api/car_park_reviews/<int:car_park_id>/sorted_by_rating_high_to_low', methods=['GET'])
def get_reviews_sorted_by_rating_high_to_low(car_space_id):
    ## Converting reviewsto dictionary lists
    reviews_list = get_sorted_reviews_by_car_space_id(car_space_id, sort_by='rating_high_to_low')

    return jsonify(reviews_list) 

@review_bp.route('/api/car_park_reviews/<int:car_park_id>/sorted_by_rating_low_to_high', methods=['GET'])
def get_reviews_sorted_by_rating_low_to_high(car_space_id):
    ## Converting reviewsto dictionary lists
    reviews_list = get_sorted_reviews_by_car_space_id(car_space_id, sort_by='rating_low_to_high')

    return jsonify(reviews_list) 

@review_bp.route('/api/car_park_reviews/<int:car_park_id>/sorted_by_time_old_to_new', methods=['GET'])
def get_reviews_sorted_by_time_old_to_new(car_space_id):
    ## Converting reviewsto dictionary lists
    reviews_list = get_sorted_reviews_by_car_space_id(car_space_id, sort_by='time_old_to_new')

    return jsonify(reviews_list) 

@review_bp.route('/api/car_park_reviews/<int:car_park_id>/sorted_by_time_new_to_old', methods=['GET'])
def get_reviews_sorted_by_time_new_to_old(car_space_id):
    ## Converting reviewsto dictionary lists
    reviews_list = get_sorted_reviews_by_car_space_id(car_space_id, sort_by='time_new_to_old')

    return jsonify(reviews_list) 

def get_sorted_reviews_by_car_space_id(car_space_id, sort_by='time_new_to_old'): 
    session = get_session()
    ## Query the database for all reviews of a specific car park space
    reviews = session.query(CarSpaceReview).filter_by(car_space_id=car_space_id).all() 

    if sort_by == 'rating_high_to_low': 
        reviews_sorted = sorted(reviews, key=lambda review: review.rating, reverse=True) 
    elif sort_by == 'rating_low_to_high': 
        reviews_sorted = sorted(reviews, key=lambda review: review.rating, reverse=False)
    elif sort_by == 'time_old_to_new': 
        reviews_sorted = sorted(reviews, key=lambda review: review.timestamp, reverse=True) 
    else:
        ## default is sorted by datetime (new to old) 
        reviews_sorted = sorted(reviews, key=lambda review: review.timestamp, reverse=False) 

    ## Converting reviewsto dictionary lists
    reviews_list = list()
    for review in reviews_sorted:
        review_dict = db_object_to_dict(review) 
        reviews_list.append(review_dict)
    session.close() 
    return jsonify(reviews_list) 

@review_bp.route('/api/car_park_reviews/<int:car_park_id>/rating_distribution', methods=['GET']) 
def get_rating_distribution(car_space_id):
    
    session = get_session() 
    reviews = session.query(CarSpaceReview).filter_by(car_space_id=car_space_id).all()  
    
    rating_distribution = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0
    }
    for review in reviews: 
        rating_distribution[str(review.rating)] += 1 
    session.close()
    return jsonify(rating_distribution) 

