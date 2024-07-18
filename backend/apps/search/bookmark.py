from database.session import get_session, engine
from database.dbTables import CarSpace, UserProfile, BookMark

def get_bookmarked_carspaces(user_id):
    """
    Gets a users bookmarked carspaces
    Args:
        user_id(int): id of user
    Output:
        List of CarSpaces a user has bookmarked
    """
    session = get_session()

    return session.query(CarSpace) \
        .select_from(BookMark) \
        .filter(BookMark.user_id==user_id, CarSpace.visibility != CarSpace.VISIBLITY_PRIVATE) \
        .join(CarSpace) \
        .all()

def register_bookmark(user_id, car_space_id):
    """
    Bookmarks a carspace for a user
    Args:
        user_id(int): id of user
    Output:
        Bool: Whether the operation was successful
    """
    session = get_session()

    new_bookmark = BookMark(
        user_id = user_id,
        car_space_id = car_space_id
    )

    try:
        session.add(new_bookmark)
        session.commit()
        return True
    except:
        return False

def delete_bookmarks(user_id, car_space_ids):
    """
    Deletes a collection of bookmarks that a user has to carspaces

    Args:
        user_id (int): id of user to whose bookmarks to delete
        car_space_ids List[int]: id of carspaces deleted by user
    Output:
        Bool: Whether the operation was successful
    """
    session = get_session()
    
    query = session.query(BookMark) \
        .filter(BookMark.user_id == user_id, BookMark.car_space_id.in_(car_space_ids))
    
    if len(query) != 0:
        try:
            query.delete()
            session.commit()
            return True
        except:
            return False
    return False