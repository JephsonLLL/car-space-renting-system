import sqlalchemy
from flask import _app_ctx_stack
from sqlalchemy.orm import sessionmaker, scoped_session
#from sqlalchemy.ext.declarative import declarative_base 

from database.dbTables import Base 


# Runs at the beginning of the program to connect to the database


## DB engine URL 
#DEFAULT_DBURL = "sqlite:///test_database.db"
DEFAULT_DBURL = "sqlite:///new_database.db"


# global variables
engine = None
LocalSession = None
#Base = declarative_base()

def create_engine(dburl=DEFAULT_DBURL):
    global engine
    global LocalSession
    engine = sqlalchemy.create_engine(dburl)
    LocalSession = sessionmaker(bind=engine)

def create_database():
    """Creates tables from the declartive base"""
    Base.metadata.create_all(get_engine()) 

# global variable getters. Wrapped in getters to support resource pools in future, if necessary
def get_engine():
    return engine

def get_session():
    return scoped_session(LocalSession)
'''
def get_declarative_base():
    return Base
'''
##create_engine()