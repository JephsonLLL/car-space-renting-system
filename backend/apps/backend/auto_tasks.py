# import os, sys 
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
# from database.session import get_session 
# from database.dbTables import Bookings, CarSpace 
# from backend.price_recommendation_system import recommend_price, recommend_price_by_car_space_id 
# from celery import Celery
# from datetime import datetime
# from enum import Enum
# from app import app

# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# @celery.task 
# def auto_update_price(): 
#     session = get_session() 
#     all_car_spaces = session.query(CarSpace).all() 
#     for car_space in all_car_spaces: 
#         if car_space.auto_price:
#             car_space.price_per_day = recommend_price_by_car_space_id(car_space_id=car_space.car_space_id) 
    
#     session.commit() 
#     session.close() 
#     return True 


# @celery.task 
# def auto_update_booking_status(): 
#     session = get_session() 
#     current_date = datetime.now().date()
#     all_bookings = session.query(Bookings).all() 
#     for booking in all_bookings: 
#         if booking.status != (Bookings.STATUS_CANCELLED or Bookings.STATUS_COMPLETE):
#             ## might need to update 
#             if current_date < booking.start_date: 
#                 booking.status = Bookings.STATUS_BOOKED 
#             elif current_date > booking.end_date: 
#                 booking.status = Bookings.STATUS_CANCELLED 
#             else: 
#                 booking.status = Bookings.STATUS_IN_PROGRESS 
#     session.commit() 
#     session.close() 
#     return True 