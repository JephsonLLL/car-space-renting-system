import requests
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from copy import deepcopy 
import statistics 
import json 
import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 

from database.dbTables import CarSpace 
import backend.utils as utils 
from database.session import get_session 

def calculate_recommended_price(width, length, car_spaces, rating=3):
    """
        Recommend price for a new car space.

        Args:
            width (float): width of the car space 
            length (float): length of the car space 
            car_spaces (list): a list of car spaces that 
                               we need to calculate the recommend price from 
            rating (int, optional): rating of the car space. Defaults to 3.

        Returns:
            float: the recommended price for the new car space 
    """
    target_area = round(float(width) * float(length),2)
    target_rating = float(rating)
    
    ## weight the price by size and rating 
    price_distribution = list()
    for car_space in car_spaces: 
        price_factor = car_space['price_per_day'] * \
                        (car_space['area']/target_area) * \
                        (car_space['rating']/target_rating) 
        ## then add it to the price distribution 
        price_distribution.append(deepcopy(price_factor)) 
    
    ## get the median and average of the price distribution 
    mean_price = statistics.mean(price_distribution) 
    median_price = statistics.median(price_distribution) 
    ## calculate the recommended price using the mean and median 
    recommened_price = (mean_price + median_price) / 2 
    
    return recommened_price  


def calculate_recommended_price_by_car_space_id(target_car_space, car_spaces): 
    """
        Recommend price for the given car space 

        Args:
            target_car_space (object): the target car space 
            car_spaces (list): a list of car spaces that 
                               we need to calculate the recommend price from 

        Returns:
            float: the recommended price for the target car space 
    """
    return calculate_recommended_price(width=target_car_space.width, 
                                       length=target_car_space.length, 
                                       car_spaces=car_spaces, 
                                       rating=target_car_space.rating) 

def recommend_price(lat, lon, width, length, school, market, public_transportation, distance=3):
    """
        Recommend price for the target car space 

        Args:
            target_car_space (CarSpace): the car space that needs a recommended price 
            distance (int, optional): radius for searching for near car spaces. Defaults to 3.

        Returns:
            float: recommended price for the target car space 
    """
     
    ## find all car spaces within a certain distance of the given address 
    car_spaces_within_distance = \
        utils.find_car_spaces_within_distance_without_id(lat=lat, 
                                                         lon=lon, 
                                                         distance=distance)
    
    ## find all car spaces with the same labels 
    car_spaces_with_same_labels = \
        utils.find_car_spaces_with_same_labels(school=school, 
                                               market=market, 
                                               public_transportation=public_transportation) 
    if len(car_spaces_within_distance) == 0 and len(car_spaces_with_same_labels) == 0: 
        ## cannot make a recommendation 
        ## calculate the mean and median of all car spaces directly 
        all_car_spaces = utils.get_all_car_spaces_info() 
        all_prices = [car_space['price_per_day'] for car_space in all_car_spaces] 
        recommended_price = (statistics.mean(all_prices) + statistics.median(all_prices)) / 2
    else:
        rec_price_list = list()
        ## calculate the recommended price using car spaces within distance 
        if len(car_spaces_within_distance) > 0:
            recommended_price_near = \
                calculate_recommended_price(width=width, length=length, 
                                            car_spaces=car_spaces_within_distance) 
            rec_price_list.append(recommended_price_near)
        ## calculate the recommended price using car spaces with same labels 
        if len(car_spaces_with_same_labels) > 0:
            recommended_price_same_labels = \
                calculate_recommended_price(width=width, length=length,
                                            car_spaces=car_spaces_with_same_labels) 
            rec_price_list.append(recommended_price_same_labels)
        ## calculate the recommended price using both the mean and the median 
        recommended_price = sum(rec_price_list)/len(rec_price_list)
    return round(recommended_price, 2)  

def recommend_price_by_car_space_id(car_space_id, distance=3): 
    session = get_session() 
    target_car_space = session.query(CarSpace).filter_by(car_space_id=car_space_id).first() 
    if not target_car_space: 
        return None 
    price = recommend_price(lat=target_car_space.lat, 
                            lon=target_car_space.lon, 
                            width=target_car_space.width, 
                            length=target_car_space.length, 
                            school=target_car_space.school, 
                            market=target_car_space.market, 
                            public_transportation=target_car_space.public_transportation, 
                            distance=distance) 
    return price

## write a main function for testing 
def main_price_recommendation(lat, lon, width, length, school, market, public_transportation, distance=3): 
    # session = get_session() 
    # target_car_space = session.query(CarSpace).filter_by(car_space_id=car_space_id).first() 
    price = recommend_price(lat, lon, width, length, school, market, public_transportation, distance=distance) 
    return price_recommendation_result_to_json(price)

## write a main function for testing 
def main_price_recommendation_by_car_space_id(car_space_id, distance=3): 
    session = get_session() 
    target_car_space = session.query(CarSpace).filter_by(car_space_id=car_space_id).first() 
    price = recommend_price_by_car_space_id(target_car_space, distance=distance) 
    return price_recommendation_result_to_json(price)

def price_recommendation_result_to_json(price): 
    result =  {"price": price, }
    return json.dumps(result) 