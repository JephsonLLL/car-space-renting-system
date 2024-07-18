# import sys 
# sys.path.append("..") 
# from backend.car_space_recommnedation_system import * 
from backend.utils import * 

## test on google api thing 
def test_google_api(): 
    ## define test address 
    test_address = "Library (F21), Library Rd, UNSW Sydney, Kensington NSW 2052"
    ## get lat and lon of address 
    lat, lon = get_lat_lon_for_address(address=test_address)
    print(lat, lon) 

## write a main function for testing 
# def test_car_space_recommendation_system():
#     ## define test address 
#     test_address = '' 
#     ## get lat and lon of address 
#     lat, lon = get_lat_lon_for_address(address=test_address)
#     ## get the session 
#     Session = sessionmaker(bind=dbsession.engine) 
#     session = Session() 
#     ## get user history 
#     user_id = 1 
#     recent_history = get_history_by_user_id(session=session, user_id=user_id, N=10) 
#     ## get user preference 
#     user_preference = get_user_preference_from_history(user_history=recent_history) 
#     ## get all car spaces 
#     all_car_spaces = get_all_car_spaces_info(session=session)
#     ## filter by distance 
#     filtered_car_spaces = find_car_spaces_within_distance_by_lat_lon(session=session, 
#                                                                      lat=lat, 
#                                                                      lon=lon, 
#                                                                      distance=5) 
#     ## get the most similar car spaces 
#     sorted_car_spaces = recommend_car_spaces_for_user(user_preference=user_preference, 
#                                                       car_space_info_list=filtered_car_spaces) 
#     ## print the result 
#     print(sorted_car_spaces) 
    
## define the main function 
if __name__ == "__main__":
    test_google_api() 
    # test_car_space_recommendation_system()