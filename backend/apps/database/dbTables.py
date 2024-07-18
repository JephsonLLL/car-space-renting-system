#import os, sys 
#sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 

from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime
from sqlalchemy import SmallInteger, BigInteger, ForeignKey, PrimaryKeyConstraint, UniqueConstraint 
from sqlalchemy.ext.declarative import declarative_base 
# from database.session import get_session 
from copy import deepcopy 
from datetime import datetime, timedelta  
#from flask_login import UserMixin

Base = declarative_base()
#Base = get_declarative_base()

## user profile table 
class UserProfile(Base):
    '''
        The user profile table. 
    '''
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False) 
    license =  Column(String(255), nullable=False) 
    # def __init__(self, first_name, last_name, phone_number, email, license, password):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.phone_number = phone_number
    #     self.email = email
    #     self.password = password
    #     self.license = license

## define a class for car space details 
class CarSpace(Base):
    """
    A carspace offered by a provider
    """
    
    #visiblility enums
    VISIBLITY_PRIVATE = 0 
    VISIBLITY_PUBLIC = 1 
    
    __tablename__ = 'car_space'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(255), nullable=False)
    # provider_id = Column(Integer, nullable=False) 
    provider_id = Column(
        Integer, 
        ForeignKey(UserProfile.id, ondelete="CASCADE"), 
        nullable=False)
    address = Column(String(255), nullable=False) 
    lat = Column(Float) 
    lng = Column(Float) 
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False) 
    price_per_day = Column(Float, nullable=False)
    available_start_date = Column(Date, nullable=False, default=datetime.now().date())
    available_end_date = Column(Date, nullable=False, default=datetime.now().date()+timedelta(days=365)) 
    booked_dates = Column(String, default='') ## store not available dates 
    tags = Column(String, default='')
    area = Column(Float) 
    school = Column(Boolean)
    market = Column(Boolean)
    public_transportation = Column(Boolean)
    auto_price = Column(Boolean)
    rating = Column(Float, default=3) 
    visibility = Column(Boolean, default=VISIBLITY_PUBLIC) 
    
    
class CarSpaceTags(Base):
    """
    A user-defined tag assigned to a carspace
    """
    __tablename__ = "car_space_tags"

    ## a one-to-one relationship 
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_space_id = Column(Integer, ForeignKey(CarSpace.id, ondelete="CASCADE"))
    
    n_rating = Column(Integer, nullable=False, default=0)
    total_rating = Column(Float, nullable=False, default=0)
    ## negative tags 
    tag_not_clean = Column(Integer, default=0) 
    tag_not_large_enough = Column(Integer, default=0) 
    tag_not_convenient = Column(Integer, default=0) 
    tag_low_quality_price_ratio = Column(Integer, default=0) 
    ## positive tags 
    tag_very_clean = Column(Integer, default=0) 
    tag_very_large = Column(Integer, default=0) 
    tag_very_convenient = Column(Integer, default=0) 
    tag_high_quality_price_ratio = Column(Integer, default=0) 
    # PrimaryKeyConstraint(car_space_id, tag) 
    def __init__(self, car_space_id):
        self.car_space_id = car_space_id
        self.n_rating = 0 
        self.total_rating = 0 
        self.tag_not_clean = 0 
        self.tag_not_large_enough = 0 
        self.tag_not_convenient = 0 
        self.tag_low_quality_price_ratio = 0 
        self.tag_very_clean = 0 
        self.tag_very_large = 0 
        self.tag_very_convenient = 0 
        self.tag_high_quality_price_ratio = 0 

    def top_N_tags(self, N=3):
        '''
            Return the top N tags for a car space 
        '''
        tags = {'tag_not_clean': self.tag_not_clean, 
                'tag_not_large_enough': self.tag_not_large_enough, 
                'tag_not_convenient': self.tag_not_convenient, 
                'tag_low_quality_price_ratio': self.tag_low_quality_price_ratio, 
                'tag_very_clean': self.tag_very_clean, 
                'tag_very_large': self.tag_very_large, 
                'tag_very_convenient': self.tag_very_convenient, 
                'tag_high_quality_price_ratio': self.tag_high_quality_price_ratio} 
        
        ## sort by number 
        sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True) 
        ## return the top N tags 
        top_N_tags = ""
        for tag in sorted_tags[:N]: 
            top_N_tags += tag[0] + ','
        return top_N_tags.strip(',') 
    
    def get_average_rating(self):
        '''
            Return the average rating for a car space 
        '''
        if self.n_rating == 0:
            return 0 
        else:
            return round(self.total_rating / self.n_rating, 1) 
        
    def update_rating(self, new_review): 

        self.n_rating += 1 
        self.total_rating += new_review.rating 
        ## negative tags 
        self.tag_not_clean += new_review.tag_not_clean 
        self.tag_not_large_enough += new_review.tag_not_large_enough
        self.tag_not_convenient += new_review.tag_not_convenient 
        self.tag_low_quality_price_ratio += new_review.tag_low_quality_price_ratio 
        ## positive tags 
        self.tag_very_clean += new_review.tag_very_clean 
        self.tag_very_large += new_review.tag_very_large 
        self.tag_very_convenient += new_review.tag_very_convenient 
        self.tag_high_quality_price_ratio += new_review.tag_high_quality_price_ratio 

## user bank details table 
class UserBankDetails(Base):
    '''
        The user bank details table. 
    '''
    __tablename__ = 'user_bank_details'

    ## this is a one-to-one relationship 
    user_id = Column(
        Integer, 
        ForeignKey(UserProfile.id, ondelete="CASCADE"), 
        primary_key=True, autoincrement=True)
    cardno = Column(BigInteger, nullable=False)
    cvv = Column(SmallInteger, nullable=False) 
    balance = Column(Float, nullable=False, default=0) 
    reward_points = Column(Integer, default=0) 
    
    # def __init__(self, user_id, cardno, cvv, balance=100, reward_points=0): 
    #     self.user_id = user_id 
    #     self.cardno = cardno 
    #     self.cvv = cvv
    #     self.balance = balance
    #     self.reward_points = reward_points 

class Vehicle(Base):
    """
    A vehicle that a user can register to the service
    """

    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    # A mant-to-one relationship
    owner = Column(Integer, ForeignKey(UserProfile.id, ondelete="CASCADE"), nullable=False)
    license_plate = Column(String, nullable=False)
    model = Column(String)

    UniqueConstraint(owner, license_plate) 
    
class Bookings(Base):
    """
    A booking made by a consumer to rent a carspace over a period
    """
    # status enums
    # booking has been made and has not began
    STATUS_BOOKED = 1 
    # booking begun and has not ended
    STATUS_IN_PROGRESS = 2
    # booking begun and ended
    STATUS_COMPLETE = 3 
    # booking has been cancelled 
    STATUS_CANCELLED = 0  

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_space_id = Column(Integer, ForeignKey(CarSpace.id, ondelete="CASCADE"))
    # provider_id = Column(Integer, ForeignKey(UserProfile.id, ondelete="CASCADE"))
    consumer_id = Column(Integer, ForeignKey(UserProfile.id, ondelete="CASCADE"))
    start_date = Column(Date)
    end_date = Column(Date) 
    distance = Column(Float)  ## this is the distance when the user search 
    duration = Column(Integer) 
    price_per_day = Column(Float) 
    tags = Column(String, default='')
    # total_price = Column(Float, nullable=False)
    # length = Column(Integer, nullable=False)
    # width = Column(Integer, nullable=False) 
    
    # ## negative tags 
    # tag_not_clean = Column(Boolean, default=False) 
    # tag_not_large_enough = Column(Boolean, default=False) 
    # tag_not_convenient = Column(Boolean, default=False) 
    # tag_low_quality_price_ratio = Column(Boolean, default=False) 
    # ## positive tags 
    # tag_very_clean = Column(Boolean, default=False) 
    # tag_very_large = Column(Boolean, default=False) 
    # tag_very_convenient = Column(Boolean, default=False) 
    # tag_high_quality_price_ratio = Column(Boolean, default=False) 
    
    status = Column(SmallInteger, nullable=False, default=STATUS_BOOKED) 
    # reward_points_used = Column(Integer, nullable=False, default=0) 
    # reward_points_earned = Column(Integer, nullable=False, default=0) 
    actual_total_price = Column(Float, default=0) 
    
    # def __init__(self, car_space_id, consumer_id, start_date, end_date, 
    #              duration, distance, car_space, car_space_tags):
        
    #     self.car_space_id = car_space_id 
    #     self.consumer_id = consumer_id 
    #     self.start_date = start_date
    #     self.end_date = end_date
    #     self.distance = distance 
        
    #     ## calculate the duration 
    #     self.duration = duration 
        
    #     ## get the provider id 
    #     self.provider_id = deepcopy(car_space.provider_id)
    #     ## use deepcopy to avoid the reference problem 
    #     self.price_per_day = deepcopy(car_space.price_per_day) 
    #     self.total_price = self.duration * self.price_per_day 
    #     self.width = deepcopy(car_space.width) 
    #     self.length = deepcopy(car_space.length) 
        
    #     ## top N tags 
    #     top_N_tags = car_space_tags.top_N_tags(N=3) 
    #     ## get the tags 
    #     self.tag_not_clean = "tag_not_clean" in top_N_tags 
    #     self.tag_not_large_enough = "tag_not large enough" in top_N_tags 
    #     self.tag_not_convenient = "tag_not_convenient" in top_N_tags 
    #     self.tag_low_quality_price_ratio = "tag_low_quality_price_ratio" in top_N_tags  
    #     self.tag_very_clean = "tag_very_clean" in top_N_tags 
    #     self.tag_very_large = "tag_very_large" in top_N_tags 
    #     self.tag_very_convenient = "tag_very_convenient" in top_N_tags 
    #     self.tag_high_quality_price_ratio = "tag_high_quality_price_ratio" in top_N_tags   
        
        ## get current timestamp 
        # current_date = datetime.now().date() 
        # if current_date < self.start_date:
        # self.status = self.STATUS_BOOKED
        # elif current_date > self.start_date and current_date < self.end_date:
        #     self.status = self.STATUS_IN_PROGRESS  
        # else: 
        #     self.status = self.STATUS_COMPLETE # this should not happen      
    # def set_reward_points_used(self, reward_points_used):
    #     self.reward_points_used = reward_points_used 
    # def set_reward_points_earned(self, reward_points_earned):
    #     self.reward_points_earned = reward_points_earned 
    # def set_actual_total_price(self, actual_total_price):
    #     self.actual_total_price = actual_total_price 

class CarSpaceReview(Base):
    __tablename__ = 'car_space_reviews'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, nullable=False) 
    consumer_id = Column(Integer, nullable=False) 
    car_space_id = Column(Integer, nullable=False) 
    provider_id = Column(Integer, nullable=False)   
    timestamp = Column(DateTime, default=datetime.now()) 
    rating = Column(Integer, nullable=False, default=5) ## default is a good experience 
    comment = Column(String) 
    ## define some tags 
    ## negative tags 
    tag_not_clean = Column(Boolean, default=False) 
    tag_not_large_enough = Column(Boolean, default=False) 
    tag_not_convenient = Column(Boolean, default=False) 
    tag_low_quality_price_ratio = Column(Boolean, default=False) 
    ## positive tags 
    tag_very_clean = Column(Boolean, default=False) 
    tag_very_large = Column(Boolean, default=False) 
    tag_very_convenient = Column(Boolean, default=False) 
    tag_high_quality_price_ratio = Column(Boolean, default=False) 

    # def __init__(self, user_id, booking_id, car_space_id, provider_id, 
    #              rating, comment, 
    #              tag_not_clean, tag_not_large_enough, tag_not_convenient, 
    #              tag_low_quality_price_ratio, tag_very_clean, tag_very_large, 
    #              tag_very_convenient, tag_high_quality_price_ratio):
        
    #     self.user_id = user_id
    #     self.booking_id = booking_id 
    #     self.car_space_id = car_space_id 
    #     self.provider_id = provider_id 
    #     self.timestamp = datetime.now() 
    #     self.rating = rating
    #     self.comment = comment 
    #     self.tag_not_clean = tag_not_clean
    #     self.tag_not_large_enough = tag_not_large_enough
    #     self.tag_not_convenient = tag_not_convenient
    #     self.tag_low_quality_price_ratio = tag_low_quality_price_ratio
    #     self.tag_very_clean = tag_very_clean
    #     self.tag_very_large = tag_very_large
    #     self.tag_very_convenient = tag_very_convenient
    #     self.tag_high_quality_price_ratio = tag_high_quality_price_ratio 
    
class BookMark(Base):
    """CarSpaces that a user has bookmarked"""
    __tablename__ = "__bookmarks__"

    user_id = Column(
        Integer,
        ForeignKey(UserProfile.id, ondelete="CASCADE"),
        nullable=False
    )
    car_space_id = Column(
        Integer,
        ForeignKey(CarSpace.id, ondelete="CASCADE"),
        nullable=False
    )

    PrimaryKeyConstraint(user_id, car_space_id)

'''
class Review(UserMixin, Base):
    """A Rating of a carspace made by a User"""

    __tablename__ = "rating"

    MAX_RATING = 5

    user_id = Column(
        Integer, 
        ForeignKey(UserProfile.id, ondelete="CASCADE"),
        primary_key = True
    )
    car_space_id = Column(
        Integer,
        ForeignKey(CarSpace.id, ondelete="CASCADE"),
        nullable=False
    )
    rating = Column(SmallInteger, nullable = False)
    datetime = Column(DateTime)
    description = Column(String)
    edited = Column(Boolean, default=False)
'''
