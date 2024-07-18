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

def sort_car_spaces(car_spaces_list, sort_by):
    if sort_by == 'distance':
        ## increasing order of distance 
        sorted_list = sorted(car_spaces_list, key=lambda x: x["distance"])
    elif sort_by == 'price': 
        sorted_list = sorted(car_spaces_list, key=lambda x: x["price_per_day"]) 
    else:
        sorted_list = sorted(car_spaces_list, key=lambda x: x["rating"], reverse=True) 
    
    return sorted_list
