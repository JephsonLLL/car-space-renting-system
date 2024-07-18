from database.dbTables import UserProfile 
from database.session import get_session

def get_user_profile_by_email(email):
    """
    gets a user's profile from their unique email address

    Args:
        email: users email to query
    Return:
        UserProfile: the users profile, if any
    """
    session = get_session()
    return session.query(UserProfile).filter_by(email=email).first()

def get_user_profile_by_id(id):
    """
    gets a user's profile from their unique user_id address

    Args:
        id: users id to query
    Return:
        UserProfile: the users profile, if any
    """
    session = get_session()
    return session.query(UserProfile).filter_by(id=id).first()

def register_new_user(email, password): 
    """
        Register a new user 

        Args:
            email (string): an email address 
            password (string): an valid password 

        Returns:
            bool: Whether the operation was successful
    """
    if get_user_profile_by_email(email=email) is not None:
        return False ## already registered 

    session = get_session()

    ## create new user and store it into database 
    new_user = UserProfile(
        first_name="",
        last_name="",
        phone_number="",
        email=email,
        license="",
        password=password
    )
    session.add(new_user)
    session.commit()
    
    return True 

def update_user_profile(id, first_name=None, last_name=None, phone_number=None, license=None):
    """
    Update the user profile. 

    Args:
        id (int): id of user to update
        first_name (string, optional): new first name. Defaults to None.
        last_name (string, optional): new last name. Defaults to None.
        phone_number (string, optional): new phone number. Defaults to None.
        license (string, optional): new license

    Returns:
        UserProfile: the resulting profile, if any. 
    """
    session = get_session()
    
    ## get the old profile
    profile = session.query(UserProfile).filter_by(id=id).first()
    if profile is not None:    ## there is a user with this id 
        ## change it into the new profile 
        profile.first_name = first_name if first_name is not None else profile.first_name
        profile.last_name = last_name if last_name is not None else profile.last_name
        profile.phone_number = phone_number if phone_number is not None else profile.phone_number
        profile.license = license if license is not None else profile.license
        session.commit()
        
        return True      
    return False    # not such a user 

def get_user_profile(id):
    """
    Gets the user profile of the user with specified. 

    Args:
        id (int): id of user to get

    Returns:
        bool: True for updated successfully, and False for not. 
    """
    session = get_session()
    return session.query(UserProfile).filter_by(id=id).first()

def delete_user(id):
    """
    Deletes a user and associated profile information. 

    Args:
        id (int): id of user to delete

    Returns:
        bool: True for deleted successfully, and False for not. 
    """

    session = get_session()

    ## get entries to delete
    profile = session.query(UserProfile).filter_by(id=id).first()

    if profile != None:
        # delete them
        session.query(UserProfile).filter_by(id=id).delete()

        session.commit()
        return True
    return False


def update_password(id, password):
    session = get_session()
    profile = session.query(UserProfile).filter_by(id=id).first()
    if profile != None:
        # delete them
        profile.password = password if password is not None else profile.password
        session.commit()
        return True
    return False
