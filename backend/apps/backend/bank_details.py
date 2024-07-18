import os, sys 
from database.session import get_session 
from database.dbTables import UserBankDetails 

def create_bank_details(user_id, cardno, cvv):
    session = get_session()
    bank_details = UserBankDetails(cardno=cardno, cvv=cvv, balance=10000)
    session.add(bank_details)
    session.commit() 
    session.close() 
    return True, "Bank details created successfully", 200 

def update_bank_details(user_id, cardno=None, cvv=None, balance=None):
    session = get_session()
    bank_details = session.query(UserBankDetails).filter_by(user_id=user_id).first()
    if not bank_details:
        return False, "Bank details not found", 404 
    bank_details.cardno = cardno if cardno else bank_details.cardno 
    bank_details.cvv = cvv if cvv else bank_details.cvv 
    bank_details.balance = balance if balance else bank_details.balance 
    session.commit() 
    session.close() 
    return True, "Bank details updated successfully", 200  

def get_bank_by_id(id):

    session = get_session()
    return session.query(UserBankDetails).filter_by(user_id=id).first()
