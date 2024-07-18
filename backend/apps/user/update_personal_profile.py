from flask import jsonify,Flask, request, Blueprint
import re

from backend.login_backend import get_user_profile_by_id,update_user_profile,get_user_profile_by_email, update_password
from flask_jwt_extended import decode_token
upp_bp = Blueprint('update_personal_profile', __name__)


@upp_bp.route('/api/update_personal_profile', methods=['POST'])
def update_personal_profile():
    
    first_name = request.json['firstname']
    last_name = request.json['lastname']
    phone = request.json['phone']
    license = request.json['carLicense']

    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    id = token["sub"]["id"]
    profile = get_user_profile_by_id(id)
    # connect with backend and update the user data
    update_user_profile(profile.id, first_name, last_name,phone,license)

    return jsonify({"msg": "success"})
        # return redirect(url_for('update_personal_profile.update_personal_profile'))

@upp_bp.route('/api/change_password', methods=['POST'])
def change_password():
    password = request.json['password']
    confirm_password = request.json['confirm_password']

    if not (password and confirm_password):
        return jsonify({"msg": "Missing fields"})

    if password != confirm_password:
        return jsonify({"msg": "Password does not match"})
    
    headers = request.headers
    authorization = headers['Authorization']
    token = decode_token(authorization)
    id = token["sub"]["id"]

    update_password(id, password)

    return jsonify({"msg": "success"})
