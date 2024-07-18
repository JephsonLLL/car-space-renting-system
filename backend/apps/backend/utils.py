import re 
import requests 
import geopy.distance 
import datetime 
from copy import deepcopy 
# from datetime import datetime 
from datetime import timedelta 
import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
from database.dbTables import CarSpace 
from database.session import get_session 

MY_GOOGLE_API_KEY = "AIzaSyDmxmrzk1HEKC7l-G4-o2QzDZdx75bgG0M" 
CAR_SPACE_TAGS = ['tag_not_clean', 'tag_not_large_enough', 'tag_not_convenient', 'tag_low_quality_price_ratio', 
                  'tag_very_clean', 'tag_very_large', 'tag_very_convenient', 'tag_high_quality_price_ratio'] 

def is_valid_email(email):
    """
    Check if an email address is valid. 
    A valid email address should be: (username)@(domain_name).(top-level_domain) 
    so it should be in pattern: (str1)@(str2).(at least 2 chars) 
    Args:
        email (str):    email address to check 

    Returns:
        result (bool):  if the given email address is valid. 
                        True for valid and False for not 
    """
    ## make sure there is no extra empty spaces
    email = email.strip(' ')
    ## define pattern of valid email address 
    pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+' 
    ## compile it 
    regex = re.compile(pattern=pattern) 
    ## check if email address is valid using the regex 
    if re.fullmatch(regex, email): 
        result = True 
    else:
        result = False 
    
    return result  

## Password Complexity Verification Function
def is_valid_password(password):
    """
        Check if a password is valid. The password must have: 
            length >= 8 
            contains at least 1 digit 
            contains at least 1 upper case letter 
            contains at least 1 lower case letter 
            contains at least 1 special character 

        Args:
            password (string): the password 
            
        Returns:
            Boolean: True for valid and False for not 
    """
    ## check the length 
    if len(password) < 8:
        return False

    ## check the if the password contains at what we need 
    if not (re.search(r'\d', password) and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[!@#$%^&*()-=_+]', password)):
        return False

    return True

## Phone Number Verification Function 
def is_australian_phone_number(phone_number):
    ## Common formats for Australian telephone numbers: 
    # +61xxxxxxxxxx, 04xxxxxxxx, 04xx xxx xxx, (04xx) xxx xxx, (02) xxxx xxxx, etc.
    au_phone_pattern = r'^(\+?61|0)[2-9]\d{8}$|^\+?61 ?4\d{2} ?\d{3} ?\d{3}$|^\+?61 ?4\d{8}$|^\((04\d{1})\) ?\d{3} ?\d{3}$|^\((02)\) ?\d{4} ?\d{4}$'

    if re.match(au_phone_pattern, phone_number):
        return True
    else:
        return False
    
def search_nearby(lat, lon, query, radius=1000):
    ##  Use the textsearch API with address or latitude/longitude as query parameters. 
    location = f'{lat},{lon}' 
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        #'query': query,
        'location': location,
        'radius': radius,  ## Search radius in metres 
        'key': MY_GOOGLE_API_KEY,
        'type': query
    }

    response = requests.get(url, params=params)
    data = response.json()
    #print(data['results'])

    if 'results' in data and len(data['results']) > 0:
        return True
    
    return False 

def check_date(date):
    if type(date) is datetime.date: 
        return date
    elif type(date) is str:
        return datetime.date.fromisoformat(date) 
    else:
        return datetime.date.fromtimestamp(date) 
    
def get_lat_lon_for_address(address): 
    ## ! working 
    """
        Get latitude and longituder for the given address using google map API. 

        Args:
            address (string): address that needs to find the lat and lon

        Returns:
            float, float: latitude and longitude of the given address. 
            None, None: if the given address cannot be found. 
    """
    ## use google maps api to get the lat and lon for the address 
    url = 'https://maps.googleapis.com/maps/api/geocode/json' 
    params = {'address': address, 'key': MY_GOOGLE_API_KEY} 
    response = requests.get(url, params=params) 
    data = response.json() 
    if data['status'] != 'OK': 
        return None, None 
    ## get latitude and longitude for the address  
    lat = data['results'][0]['geometry']['location']['lat'] 
    lon = data['results'][0]['geometry']['location']['lng'] 
    return lat, lon 

def calculate_distance(lat1, lon1, lat2, lon2): 
    # ! working 
    """
        Calculate distance between two points using latitude and longitude.  

        Args:
            lat1 (float): latitude of the first point
            lon1 (float): longitude of the first point
            lat2 (float): latitude of the second point
            lon2 (float): longitude of the second point

        Returns:
            float: distance between two points in km. 
    """
    ## calculate distance in km 
    return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).km 

def get_all_car_spaces_info(): 
    """
        Get all car space info from the CarSpace table. 

        Returns:
            list: list of all car space info. 
    """ 
    session = get_session() 
    car_space_list = session.query(CarSpace).all() 
    result_list = [{key: value for key, value in row.__dict__.items() if not key.startswith('_')} for row in car_space_list]
    return result_list 

def find_car_spaces_within_distance(consumer_id, lat, lon, distance): 
    """
        Use google maps API to find all car spaces within a certain distance of a given address 

        Args:
            session (sqlalchemy session): current session 
            address (string): address of the target car space 
            distance (float): distance in km that the car spaces need to be within 

        Returns:
            list: list of all car spaces within the given distance of the given address. 
    """
    session = get_session()
    
    ## get all car spaces from the database 
    car_spaces = get_all_car_spaces_info() 
    ## find all car spaces within the given distance 
    car_spaces_within_distance = [] 
    for car_space in car_spaces: 
        if (car_space['visibility'] == CarSpace.VISIBLITY_PRIVATE) or (car_space['provider_id'] == consumer_id):
            continue 
        actual_distance = calculate_distance(lat1=lat, 
                                             lon1=lon, 
                                             lat2=car_space['lat'], 
                                             lon2=car_space['lng']) 
        if actual_distance <= float(distance): 
            car_space['distance'] = actual_distance 
            # car_space_dict = db_object_to_dict(car_space)
            car_spaces_within_distance.append(car_space) 
    
    return car_spaces_within_distance 

def find_car_spaces_within_distance_without_id(lat, lon, distance): 
    """
        Use google maps API to find all car spaces within a certain distance of a given address 

        Args:
            session (sqlalchemy session): current session 
            address (string): address of the target car space 
            distance (float): distance in km that the car spaces need to be within 

        Returns:
            list: list of all car spaces within the given distance of the given address. 
    """
    session = get_session()
    
    ## get all car spaces from the database 
    car_spaces = get_all_car_spaces_info() 
    ## find all car spaces within the given distance 
    car_spaces_within_distance = [] 
    for car_space in car_spaces: 
        if (car_space['visibility'] == CarSpace.VISIBLITY_PRIVATE):
            continue 
        actual_distance = calculate_distance(lat1=lat, 
                                             lon1=lon, 
                                             lat2=car_space['lat'], 
                                             lon2=car_space['lng']) 
        if actual_distance <= float(distance): 
            car_space['distance'] = actual_distance 
            # car_space_dict = db_object_to_dict(car_space)
            car_spaces_within_distance.append(car_space) 
    
    return car_spaces_within_distance 

# def find_car_spaces_within_distance_by_lat_lon(lat, lon, distance): 
#     """
#         Use google maps API to find all car spaces within a certain distance of a given address 

#         Args:
#             session (sqlalchemy session): current session 
#             lat(float): target latitude 
#             lon(float): target longitude 
#             distance (float): distance in km that the car spaces need to be within 

#         Returns:
#             list: list of all car spaces within the given distance of the given address. 
#     """
#     session = get_session()
#     ## get all car spaces from the database 
#     car_spaces = get_all_car_spaces_info() 
#     ## find all car spaces within the given distance 
#     car_spaces_within_distance = [] 
#     for car_space in car_spaces: 
#         if calculate_distance(lat1=lat, 
#                               lon1=lon, 
#                               lat2=car_space.lat, 
#                               lon2=car_space.lon) <= distance: 
#             car_spaces_within_distance.append(car_space) 
#     return car_spaces_within_distance 

def find_car_spaces_with_same_labels_by_car_space_id(target_car_space): 
    """
        Find all car spaces have same labels with the given car space

        Args:
            session (sqlalchemy session): current session 
            target_car_space (object): object of CarSpace class 

        Returns:
            list: a list of all car spaces with the same labels with the given car space. 
    """
    session = get_session() 
    ## filter out all car spaces with the same labels 
    car_spaces_with_same_labels = session.query(CarSpace).filter(
        CarSpace.school == target_car_space.school,
        CarSpace.market ==  target_car_space.market,
        CarSpace.public_transportation == target_car_space.public_transportation
    ).all()

    return car_spaces_with_same_labels 

def find_car_spaces_with_same_labels(school, market, public_transportation): 
    """
        Find all car spaces have same labels with the given car space

        Args:
            session (sqlalchemy session): current session 
            target_car_space (object): object of CarSpace class 

        Returns:
            list: a list of all car spaces with the same labels with the given car space. 
    """
    session = get_session() 
    ## filter out all car spaces with the same labels 
    car_spaces_with_same_labels = session.query(CarSpace).filter(
        CarSpace.school == school,
        CarSpace.market == market,
        CarSpace.public_transportation == public_transportation
    ).all() 

    res = list()
    for car_space in car_spaces_with_same_labels:
        car_space_dict = db_object_to_dict(car_space) 
        res.append(car_space_dict)
    return res 

def db_object_to_dict(db_object): 
    """
        Convert a database object to a dictionary. 

        Args:
            db_object (object): database object 

        Returns:
            dict: dictionary of the database object 
    """
    return {key: value for key, value in db_object.__dict__.items() if not key.startswith('_')} 

def get_duration_in_days(start_date, end_date): 
    """
        Calculate the duration between two dates. 

        Args:
            start_date (datetime.date): start date 
            end_date (datetime.date): end date 

        Returns:
            float: duration in days 
    """
    return (end_date - start_date).days+1 

def get_in_range_date(start_date, end_date): 
    start_date = check_date(start_date) 
    end_date = check_date(end_date)
    dates_in_range = []
    current_date = start_date

    while current_date <= end_date:
        dates_in_range.append(current_date)
        current_date += timedelta(days=1)

    return dates_in_range 

def get_weekday(date): 
    """
        Get the weekday of the given date. 

        Args:
            date (datetime.date): date 

        Returns:
            string: the weekday of the given date 
    """
    return date.weekday() 

def get_available_car_space(start_date, end_date, car_space_list):
    """_summary_

    Args:
        start_date (_type_): _description_
        end_date (_type_): _description_
        car_space_list (list): list of dict 

    Returns:
        _type_: _description_
    """
    selected_date_list = get_in_range_date(start_date, end_date) 
    available_car_space_list = [] 
    ## get the start_date and the end_date in dtae format
    start_date = check_date(start_date)
    end_date = check_date(end_date)
    for car_space in car_space_list: 
        if (start_date >= check_date(car_space['available_start_date']) 
            and end_date <= check_date(car_space['available_end_date'])):
            ## get booked dates 
            if len(car_space['booked_dates']) > 0:
                booked_dates_date = [check_date(date) for date in car_space['booked_dates'].split(',')]  
                ## make sure the selected date is not in booked dates 
                if not have_same_element(selected_date_list, booked_dates_date): 
                    available_car_space_list.append(car_space) 
            else:
                available_car_space_list.append(car_space) 
        
    return available_car_space_list    

def get_boolean_tags(tags): 
    tags = tags.split(',') 
    boolean_tags = dict() 
    for tag in CAR_SPACE_TAGS:
        if tag in tags: 
            boolean_tags[tag] = 1 
        else:
            boolean_tags[tag] = 0 
    
    return boolean_tags 

def have_same_element(l1, l2): 
    for element in l1:
        if element in l2:
            return True 
    return False 