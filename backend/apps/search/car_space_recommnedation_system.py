'''
    Car space recommendation system                
    A subsystem of car space renting system  
    Written by Shu WANG (z5211077)                       
    Last Modified on 02/07/2023 
'''
import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 

import json 
import numpy as np 
from copy import deepcopy 
from sqlalchemy import desc 
from sqlalchemy.orm import sessionmaker
from sklearn.metrics.pairwise import cosine_similarity 

from backend.utils import * 
from database.dbTables import Bookings, CarSpaceTags  
from database.session import get_session 

DEFAULT_PREFERENCE = { 'distance':3, 
                        'length':3,
                        'width':2, 
                        'price_per_day':15, 
                        'rating': 5, 
                        'tag_not_clean':0.5, 
                        'tag_not_large_enough':0.5,
                        'tag_not_convenient':0.5,
                        'tag_low_quality_price_ratio':0.5,
                        'tag_very_clean':0.5,
                        'tag_very_clean':0.5,
                        'tag_very_large':0.5,
                        'tag_very_convenient':0.5,
                        'tag_high_quality_price_ratio':0.5}

CAR_SPACE_FEATURES = ['distance', 'length', 'width', 'price_per_day', 'rating', 
                      'tag_not_clean', 'tag_not_large_enough', 'tag_not_convenient', 'tag_low_quality_price_ratio', 
                      'tag_very_clean', 'tag_very_large', 'tag_very_convenient', 'tag_high_quality_price_ratio'] 
CAR_SPACE_TAGS = ['tag_not_clean', 'tag_not_large_enough', 'tag_not_convenient', 'tag_low_quality_price_ratio', 
                  'tag_very_clean', 'tag_very_large', 'tag_very_convenient', 'tag_high_quality_price_ratio'] 

def get_history_by_user_id(user_id, N=10): 
    """
        Get `N` most recent user history of `user_id` from the Bookings table.

        Args:
            user_id (int): user id of the user we want to search. 
            N (int, Optional): number of most recent history we want. Default to 10. 
        Returns:
            list: list of user's N most recent booking history (dict). 
    """
    session = get_session()
    recent_history = session.query(Bookings)\
                     .filter((Bookings.consumer_id==user_id and Bookings.status!=Bookings.STATUS_CANCELLED))\
                         .order_by(desc(Bookings.end_date))\
                             .limit(N)\
                                 .all() 
    # result_list = [row.__dict__ for row in recent_history] 
    result_list = [db_object_to_dict(row) for row in recent_history] 
    ## get width and length 
    for res in result_list: 
        ## get the car space 
        car_space = session.query(CarSpace).filter_by(id=res['car_space_id']).first() 
        res['width'] = deepcopy(car_space.width) 
        res['length'] = deepcopy(car_space.length) 
        res['rating'] = deepcopy(car_space.rating)
        car_tags_dict = get_boolean_tags(tags=res['tags']) 
        for k,v in car_tags_dict.items():
            res[k] = v 
    session.close()
    return result_list # list of dict 

def get_user_preference_from_history(user_history, weighted=True, decay_factor=0.8): 
    """
        Get the weighted average of features from the user's history as the user's preference. 

        Args:
            user_history (list): A list of user histories (dict). 
            weighted (bool, optional): If the average should be weighted. Defaults to True.
            decay_factor (float, optional): the weight decay factor. Defaults to 0.8.

        Returns:
            dict: user's preference. 
    """
    ## change the decay factor into 1 if we do not want weighted average 
    if not weighted:
        decay_factor = 1.0
    
    ## define our features 
    features = deepcopy(CAR_SPACE_FEATURES) 
    
    ## then calculate the average of features 
    ## make a dictory for history_values

    if len(user_history) == 0: 
        return DEFAULT_PREFERENCE
    history_values = dict() 
    for feature in features: 
        history_values[feature] = list()
    ## get the sum 
    for history in user_history: 
        for feature in history_values:
            if feature == 'distance': 
                value = history[feature] if history[feature] is not None else 3 
            else:
                value = history[feature] 
            ## since we don't know the attribute name, we need to use getattr to get the value
            history_values[feature].append(value) 
    
    ## then get the weighted preference 
    preference = dict() 
    for feature in features: 
        # print(history_values)
        preference[feature] = \
            calculate_weighted_feature(value_list=history_values[feature], 
                                       decay_factor=decay_factor)

    return preference 

def calculate_weighted_feature(value_list, decay_factor=0.8): 
    """
        Calculate weight feature 

        Args:
            value_list (list): a list of values for one feature. 
            decay_factor (float, optional): value of the decay factor, 
                                            should be between 0 to 1. Defaults to 0.8.

        Returns:
            float: weight feature value
    """
    weighted_sum = 0 
    total_weight = 0 
    weighted_result = 0 
    for i, v in enumerate(value_list):
        if v is not None:
            ## calculate the weight 
            ## most recent history will have higher weight 
            weight = decay_factor**i  
            weighted_sum += v*weight 
            total_weight += weight 
    
    if total_weight != 0:
        weighted_result = weighted_sum / total_weight
    else:
        weighted_result = 0 
        
    return weighted_result

def calculate_user_single_car_space_similarity(user_preference, car_space_info, 
                                               features, user_vector=None): 
    """
        Calculate the similarity between a user and a car space. 

        Args:
            user_preference (dict): preference of a user 
            car_space_info (object): the information of a single car space 
            features (list): a list of features. 
            user_vector (np.array, optional): vector of the user's preference. Defaults to None.
            
        Returns:
            float: similarity between the user and the car space. 
    """
    if user_vector is None:
        ## calculate user vector and car park vector 
        ## need to reshape 
        user_vector = np.array([user_preference[feature] for feature in features]).reshape(1, -1)
    
    car_space_vector = np.array([car_space_info[feature] for feature in features]).reshape(1, -1) 
    ## calculate the cosine similarity 
    similarity = cosine_similarity(X=user_vector, Y=car_space_vector) 
    return similarity[0][0]

def recommend_car_spaces_for_user(user_preference, car_space_info_list): 
    """
        Calculates the similarity between a user and all filtered spaces 
        and returns the spaces in order of similarity.

        Args:
            user_preference (dict): preference of the user 
            car_space_info_list (list): a list of car spaces filtered by distance and availalble time. 

        Returns:
            list: a list of car spaces sorted by similarity. 
    """
    
    ## get car space features, and delete the id 
    features = list(user_preference.keys()) 
    
    ## use a list to store result 
    similarity_list = list()
    
    ## get user vector 
    user_vector = np.array([user_preference[feature] for feature in features]).reshape(1, -1)
    
    ## then go through all car spaces 
    for car_space_info in car_space_info_list:
        similarity = \
            calculate_user_single_car_space_similarity(user_preference=user_preference, 
                                                       car_space_info=car_space_info, 
                                                       features=features, 
                                                       user_vector=user_vector)
        ## add the similarity to the similarity list 
        similarity_list.append([car_space_info, similarity])
    
    ## sort the similarity list with similarity in descending order 
    sorted_similarities = sorted(similarity_list, key=lambda x: x[1], reverse=True)
    ## then get the car space info 
    sorted_car_spaces = [car_space_similarity[0] for car_space_similarity in sorted_similarities]
    # print(sorted_car_spaces)
    return sorted_car_spaces, sorted_similarities 

def find_similar_car_spaces(target_car_space_info, car_spaces_info_list): 
    # ! not using  now 
    """
        The `recommend_car_spaces_for_user` function could also be used for recommending similar car spaces. 
        But we need to think about the distance 
        Args:
            target_car_space_info (dict): information of a single car space. 
            car_space_info_list (list): a list of car spaces filtered by distance. 

        Returns:
            list: a list of car spaces sorted by similarity. 
    """
    ## get tags 
    
    return recommend_car_spaces_for_user(user_preference=target_car_space_info, 
                                         car_space_info_list=car_spaces_info_list) 

def main_car_space_recommendation(user_id, filtered_car_spaces):
    recent_history = get_history_by_user_id(user_id=user_id, N=10) 
    ## get user preference 
    user_preference = get_user_preference_from_history(user_history=recent_history) 
    ## get tags 
    session = get_session()
    for car_space in filtered_car_spaces:
        car_space_tags = session.query(CarSpaceTags).filter_by(car_space_id=car_space['id']).first() 
        ## get top N tags 
        top_N_tags = car_space_tags.top_N_tags(N=3)
        for tag_feature in CAR_SPACE_TAGS:
            if tag_feature in top_N_tags:
                car_space[tag_feature] = True 
            else:
                car_space[tag_feature] = False 
    ## get the most similar car spaces 
    sorted_car_spaces, sorted_similarities = \
        recommend_car_spaces_for_user(user_preference=user_preference, 
                                      car_space_info_list=filtered_car_spaces) 
    
    
    #return car_space_result_to_json(sorted_car_spaces=sorted_car_spaces)
    return sorted_car_spaces

def car_space_result_to_json(sorted_car_spaces): 
    ## find the car space info from the db by id 
    car_space_info_list = list()
    session = get_session() 
    for car_space in sorted_car_spaces: 
        car_space_info = session.query(CarSpace).filter_by(id=car_space['id']).first() 
        car_space_info = db_object_to_dict(car_space_info) 
        if car_space_info is not None: 
            car_space_info_list.append(car_space_info) 
    ## change the list into json 
    for car_space in car_space_info_list:
        car_space['available_start_date'] = car_space['available_start_date'].strftime('%Y-%m-%d')
        car_space['available_end_date'] = car_space['available_end_date'].strftime('%Y-%m-%d')

    car_space_info_json = json.dumps(car_space_info_list) 
    session.close()
    return car_space_info_json 

                                          
                                     
                                                        