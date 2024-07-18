from flask import flash, jsonify, Flask, abort, Blueprint, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from backend.login_backend import get_user_profile_by_id,get_user_profile_by_email,register_new_user, update_user_profile
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required


import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 
from backend.login_backend import get_user_profile_by_id,get_user_profile_by_email,register_new_user, update_user_profile
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required
from backend.utils import is_valid_email, is_valid_password, is_australian_phone_number 
from backend.bank_details import create_bank_details 


'''
@user_bp.route('/login')
def login():
    return render_template('login.html')
'''

login_bp = Blueprint('login', __name__)
@login_bp.route('/api/login',  methods=['POST'])
def login():
    # login code goes here
    data = request.get_json()
    email = data.get('email', None) 
    password = data.get('password', None) 
    if not (email and password):
        return jsonify({'error': 'Missing fields'}), 400 
    user = get_user_profile_by_email(email)
    if not user or not user.password == password:
        return jsonify({"msg": "Wrong username or password"}), 401
    access_token = create_access_token(identity={"id": user.id})
    return jsonify(access_token=access_token)

logout_bp = Blueprint('logout', __name__)
@logout_bp.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


signup_bp = Blueprint('signup', __name__)
@signup_bp.route('/api/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.json.get('email')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    password = request.json.get('password')
    license = request.json.get('carlicense')
    phone = request.json.get('phoneNumber')
    #confirm_password = request.json.get('confirm_password') 
    card_number = request.json.get('bankAccount')
    cvv = request.json.get('csv') 

    register_new_user(email,password)

    profile = get_user_profile_by_email(email)
    update_user_profile(profile.id, firstname, lastname, phone, license)
    
    # create bank account 
    res, msg, status = create_bank_details(user_id=profile.id, 
                                           cardno=card_number, 
                                           cvv=cvv)
    
    access_token = create_access_token(identity={"id": profile.id})
    return jsonify(access_token=access_token) 

    # return jsonify({'message': 'User created successfully'}), 201
