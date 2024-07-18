import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
from datetime import datetime, timedelta 
from database.dbTables import CarSpace, CarSpaceTags
from database.session import get_session
from backend.utils import get_lat_lon_for_address, search_nearby 
from backend.price_recommendation_system import main_price_recommendation, price_recommendation_result_to_json 
# def register_new_car_space(provider, 
#                            address, 
#                            lat,
#                            lng,
#                            length,
#                            width,  
#                            price,
#                            available_start_date, 
#                            available_end_date, 
#                            #visibility = CarSpace.VISIBLITY_PRIVATE
#                            ):
#     """
#     Creates a new carspace

#     Args:
#         name (int): name of the car space to create
#         provider (int): user_id of the provider of this car space
#         address (string): address of the car space
#         available_start_date (datetime.date): start date that car space available. Expects a python datetime.date type
#         available_end_date Variant[string, date]: date that car space is no longer available. Expects a python datetime.date type
#         price_per_day (int): cost of the carspace
#         size Optional(float): space of car space in square meters
#         visibility Optional(bool): whether public can see this car space
    
#     Returns:
#         True if sucessful,
#         False if unsucessful
#     """
#     session = get_session()

#     new_car_space = CarSpace(
#         provider_id = provider,
#         address = address,
#         lat = lat,
#         lng = lng,
#         length = length,
#         width = width,
#         price_per_day = price, 
#         available_start_date = available_start_date,
#         available_end_date = available_end_date,
#         #visibility = visibility
#     )
#     session.add(new_car_space)
#     session.commit() 
#     # create car space tags
#     car_space = session.query(CarSpace).filter(CarSpace.address == address, CarSpace.provider_id == provider).first()
#     tags = CarSpaceTags(car_space_id = car_space.id)
#     session.add(tags)
#     session.commit()
#     session.close()
#     return True 

def register_new_car_space(provider, address, lat, lng, length, width, price, auto_price,  
                           available_start_date=None, available_end_date=None, available_days=None, 
                           visibility=None):
    """
    Creates a new carspace

    Args:
        name (int): name of the car space to create
        provider (int): user_id of the provider of this car space
        address (string): address of the car space
        available_start_date (datetime.date): start date that car space available. Expects a python datetime.date type
        available_end_date Variant[string, date]: date that car space is no longer available. Expects a python datetime.date type
        price_per_day (int): cost of the carspace
        size Optional(float): space of car space in square meters
        visibility Optional(bool): whether public can see this car space
    
    Returns:
        True if sucessful,
        False if unsucessful
    """
    session = get_session() 
    
    car_space = session.query(CarSpace).filter(CarSpace.address==address).first() 
    if car_space:
        return False, "This car space already registered.", 409 
    ## get the latitude and longitude using address 
    #lat, lng = get_lat_lon_for_address(address=address) 
    ## calculate the area of the car space 
    area = round(float(width) * float(length), 2)  
    school = search_nearby(lat=lat, lon=lng, radius=500, query="school") 
    market = search_nearby(lat=lat, lon=lng, radius=500, query="supermarket") 
    public_transportation = search_nearby(lat=lat, lon=lng, radius=500, query="bus_station") 
    
    ## set default values for available_start_date, available_end_date, available_days
    visibility = CarSpace.VISIBLITY_PUBLIC if visibility is None else visibility 
    # available_start_date = datetime.now().date() if available_start_date is None else available_start_date 
    # available_end_date = available_start_date + timedelta(days=100) if available_end_date is None else available_end_date 
    # available_days = '0,1,2,3,4,5,6' if available_days is None else available_days 
    
    ## create a new car space object 
    new_car_space = CarSpace(
        provider_id = provider,
        address = address,
        lat = lat,
        lng = lng,
        length = length,
        width = width, 
        area = area, 
        school = school,
        market = market,
        public_transportation = public_transportation,
        price_per_day = price, 
        auto_price = auto_price, 
        available_start_date = available_start_date,
        available_end_date = available_end_date, 
        # available_days = available_days,
        #visibility = visibility
    )
    
    session.add(new_car_space) 
    session.commit() 
    ## create car space tags for this car space 
    car_space = session.query(CarSpace).filter(CarSpace.address == address, CarSpace.provider_id==provider).first()
    new_car_space_tags = CarSpaceTags(car_space_id=car_space.id)
    session.add(new_car_space_tags) 
    ## commit changes  
    session.commit() 
    session.close() 

    return True, "Successfully registered a new car space.", 200  


def update_car_space(car_space_id, 
                           address, 
                           lat,
                           lng,
                           length,
                           width,  
                           price,
                           available_start_date, 
                           available_end_date, ):
    """
    Updates a registered carspace

    Args:
        car_space_id (int): id of the carspace to update
        address (string):
        available_start_date (datetime.date): start date that car space available. Expects a python datetime.date type
        available_end_date Variant[string, date]: date that car space is no longer available. Expects a python datetime.date type
        price_per_day (int): cost of the carspace
        size Optional(float): space of car space in square meters
        visibility Optional(bool): whether public can see this car space
    Returns:
        bool: Whether the carspace was successfully updated
    """
    session = get_session()

    car_space = session.query(CarSpace).filter_by(id=car_space_id).first()
    if car_space is not None:
        car_space.address = address if address is not None else car_space.address
        car_space.available_start_date = available_start_date if available_start_date is not None else car_space.available_start_date
        car_space.available_end_date = available_end_date if available_end_date is not None else car_space.available_end_date
        car_space.price = price if price is not None else car_space.price
        car_space.length = length if length is not None else car_space.length
        car_space.width = width if width is not None else car_space.width
        car_space.lat = width if lat is not None else car_space.lat
        car_space.lng = width if lng is not None else car_space.lng     
        # car_space.visibility = visibility if visibility is not None else car_space.visibility

        session.commit()
        return True
    return False

def get_provider_car_spaces(provider_id):
    """
    Gets a providers registered carspace and their details

    Args:
        provider_id (int): user_id of the provider to get the carspaces of
    
    Returns:
        List[CarSpace]: all the providers registed carspaces, if any
    """

    session = get_session()
    all_car_spaces = session.query(CarSpace).filter_by(provider_id = provider_id).all()
    ret = []
    for c in all_car_spaces:
        c_todict = {key: value for key, value in c.__dict__.items() if not key.startswith('_')}
        ret.append(c_todict)
    return ret

def delete_car_space(car_space_id):
    """
    Deletes a specified Car space
    
    Args:
        car_space_id (int): id of the car_space to get rid of
    
    Returns:
        bool: whether the carspace was deleted by this operation
    """

    session = get_session()

    query = session.query(CarSpace).filter_by(id = car_space_id)   
    if query.first() != None:
        query.delete()
        session.commit()
        print("delete success")
        return True
    return False

'''
def get_car_space_tags(car_space_id):
    """
    Gets the consumer-defined tags assigned to a car space

    Args:
        car_space_id (int): id of the car_space to get the tags of
    
    Returns:
        List[string]: all the carspaces registered tags, if any
    """

    session = get_session()

    return list(session.query(CarSpaceTags)\
        .filter_by(car_space=car_space_id)\
        .map(lambda entry: entry.tag))

'''

def get_car_space_by_id(id):
    """
    gets a car space from their unique car_space_id address

    Args:
        id: car_space_id to query
    Return:
        CarSpace: the CarSpace profile, if any
    """
    session = get_session()
    return session.query(CarSpace).filter_by(id=id).first()

def recommend_price_carspace(lat,lng, length, width): 
    #lat, lng = get_lat_lon_for_address(address=address) 
    #import pdb
    #pdb.set_trace()

    school = search_nearby(lat=lat, lon=lng, radius=500, query="school") 
    market = search_nearby(lat=lat, lon=lng, radius=500, query="supermarket")
    public_transportation = search_nearby(lat=lat, lon=lng, radius=500, query="bus_station") 
    
    #school,market,public_transportation = True,True,True
    
    distance = 3 
    recommended_price = main_price_recommendation(lat=lat, lon=lng, width=width, length=length, 
                                                  school=school, market=market, public_transportation=public_transportation, 
                                                  distance=distance) 
    return price_recommendation_result_to_json(recommended_price)