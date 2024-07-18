import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
from database.dbTables import Bookings, CarSpace, UserProfile, UserBankDetails, CarSpaceTags 
from database.session import get_session #, get_declarative_base
from backend.utils import get_duration_in_days, check_date, get_in_range_date 
from copy import deepcopy 
from datetime import datetime 
from backend.login_backend import get_user_profile_by_id
from backend.carspace import get_car_space_by_id
from backend.bank_details import get_bank_by_id

def make_booking(car_space_id, consumer_id, start_date, end_date, distance):
    """
        Create a new booking

        Args:
            car_space_id (int): id of the carspace this booking made to
            consumer_id (int): user_id of the consumer this booking is made for
            start_date (datetime.date): starting date of the rent for this booking
            end_date (datetime.date): final date of the rent for this booking
        Returns:
            bool: Whether the booking was actually created
    """
    ## get db session 
    ## get car space information 
    session = get_session()

    ## get the dates between start date and end date 
    booking_dates = get_in_range_date(start_date, end_date) 
    ## get the car space 
    car_space = session.query(CarSpace).filter_by(id=car_space_id).first()  
    user = get_user_profile_by_id(consumer_id)
    # provider = get_user_profile_by_id(car_space.provider_id)
    if not car_space:
        return False, "Car space not found.", 404 
    if not user: 
        return False, "User not found.", 404  
    ## add the booked dates to the car space 
    car_space_booked_dates = deepcopy(car_space.booked_dates.split(',')) 
    current_date = datetime.now().date() 
    new_booked_dates = '' 
    for booked_date in car_space_booked_dates: 
        if len(booked_date) == 0: 
            continue
        booked_date_date = check_date(booked_date) 
        ## delete the date if it is before today to avoid making the booked_dates too long
        if booked_date_date < current_date: 
            continue 
        ## delete the date if it is already booked
        if booked_date_date in booking_dates: 
            return False, "The dates you selected are already booked.", 400
        new_booked_dates += str(booked_date) + ',' 
    ## add the dates in this booking into the car space information 
    for booking_date in booking_dates: 
        new_booked_dates += str(booking_date) + ',' 
    ## update the car space information 
    car_space.booked_dates = new_booked_dates.strip(',')
    session.commit() 
    ## update the car space
    start_date = check_date(start_date) 
    end_date = check_date(end_date) 
    duration = get_duration_in_days(start_date, end_date)
    # car_space_tags = session.query(CarSpaceTags).filter_by(car_space_id=car_space_id).first()
    new_booking = Bookings(car_space_id=car_space_id, 
                           consumer_id=consumer_id, 
                           start_date=start_date, 
                           end_date=end_date, 
                           duration=duration, distance=float(distance),price_per_day=car_space.price_per_day)
    
    ## update consumer and provider's balance 
    ## get consumer's profile 
    consumer_bank_details = session.query(UserBankDetails).filter_by(user_id=consumer_id).first()
    ## get provider's profile
    provider_bank_details = session.query(UserBankDetails).filter_by(user_id=car_space.provider_id).first()
    ## calculate the number of reward points could be used 
    booking_price = duration * car_space.price_per_day
    # max_rp = int(booking_price) 
    # if consumer_bank_details.reward_points >= max_rp:
    #     rp_used = max_rp 
    # else: 
    #     rp_used = consumer_bank_details.reward_points 
    
    actual_booking_price = booking_price - consumer_bank_details.reward_points
    ## update the balance and reward points of consumer 
    consumer_bank_details.balance -= actual_booking_price 
    consumer_bank_details.reward_points = actual_booking_price * 0.1 
    # consumer_bank_details.reward_points += int(actual_booking_price) 

    ## update the balance of provider 
    provider_bank_details.balance += booking_price * 0.8

    # new_booking.set_reward_points_used(rp_used) 
    new_booking.actual_total_price = actual_booking_price
    # new_booking.set_reward_points_earned(int(booking_total_price)) 
    
    ## commit to database 
    session.add(new_booking)
    session.commit()

    session.close()
    return True, "Booking created successfully", 200  


def cancel_booking(booking_id):
    """
    Cancel a booking

    Args:
        booking_id (int): id of the booking to cancel
    Returns:
        bool Whether the booking was actually cancelled
    """
    
    ## get the session 
    session = get_session() 
    ## get the booking 
    booking = session.query(Bookings).filter_by(id=booking_id).first() 
    
    ## get the date to decide if penalty is applied 
    current_date = datetime.now().date() 
    flag_penalty = False 
    if current_date > booking.start_date: 
        ## cannot cancel the booking if the booking has already started 
        return -1, "Cannot cancel the booking if the booking has already started.", 400 
    else: 
        n_days_in_advance = get_duration_in_days(current_date, booking.start_date)  
        if n_days_in_advance < 1:
            flag_penalty = True 
    
    ## update the booking id 
    if booking.status == Bookings.STATUS_CANCELLED: 
        return False, "Booking has already been cancelled.", 409 
    ## could cancel 
    booking.status = Bookings.STATUS_CANCELLED 
    
    ## delete the booked_dates in the car space 
    booking_dates = get_in_range_date(start_date=booking.start_date, end_date=booking.end_date) 
    ## get the car space and the booked dates 
    car_space = session.query(CarSpace).filter_by(id=booking.car_space_id).first() 
    car_space_booked_dates = deepcopy(car_space.booked_dates.split(',')) 
    new_booked_dates = '' 
    for booked_date in car_space_booked_dates: 
        if len(booked_date) == 0: 
            continue 
        booked_date_date = check_date(booked_date) 
        ## delete the date if it is already booked
        if booked_date_date in booking_dates: 
            continue
        new_booked_dates += str(booked_date) + ',' 
    ## update the car space information 
    car_space.booked_dates = new_booked_dates.strip(',') 
    session.commit() 
    ## return the money to the consumer 
    ## get consumer's profile 
    consumer_bank_details = session.query(UserBankDetails).filter_by(user_id=booking.consumer_id).first() 
    ## get provider's profile
    provider_bank_details = session.query(UserBankDetails).filter_by(user_id=car_space.provider_id).first() 
    
    ## 20% penalty 
    if flag_penalty: 
        refund_price = deepcopy(booking.actual_total_price * 0.8)  
        provider_bank_details.balance += booking.actual_total_price - refund_price 
        
    else: 
        refund_price = deepcopy(booking.actual_total_price) 
        
    ## return the money to the consumer 
    consumer_bank_details.balance += refund_price 
    ## delete the rewards point earned from this booking 
    consumer_bank_details.reward_points -= deepcopy(booking.reward_points_earned) 
    ## return the reward points used to the provider 
    consumer_bank_details.reward_points += deepcopy(booking.reward_points_used) 
    ## get the moneny back 
    provider_bank_details.balance -= deepcopy(round(booking.total_price * 0.8, 2)) 
    
    session.commit() 
    session.close() 
    return True, "Booking cancelled successfully!", 200 


def get_bookings(id):
    session = get_session()
    all_car_spaces = session.query(Bookings).filter_by(consumer_id=id).all()
    ret = []
    for c in all_car_spaces:
        c_todict = {key: value for key, value in c.__dict__.items() if not key.startswith('_')}
        ret.append(c_todict)
    return ret
