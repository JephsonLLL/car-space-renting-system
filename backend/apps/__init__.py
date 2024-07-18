from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

from user.view import login_bp, logout_bp, signup_bp 
from car.view import car_bp
from user.update_personal_profile import upp_bp
from booking.view import booking_bp
from review.view import write_review_bp, review_bp 
from search.view import search_bp
import settings

def create_app():
   app = Flask(__name__)
   jwt = JWTManager()

   app.config.from_object(settings)
   app.config["JWT_SECRET_KEY"] = "abcd"
   app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
   #app.secret_key = 'ChangeMe!'
   #app.config['JWT_BLACKLIST_ENABLED'] = True
   #app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

   jwt.init_app(app)

   app.register_blueprint(login_bp) 
   app.register_blueprint(logout_bp) 
   app.register_blueprint(signup_bp) 
   
   app.register_blueprint(car_bp)
   
   app.register_blueprint(upp_bp)
   
   app.register_blueprint(search_bp) 
   app.register_blueprint(booking_bp) 

   
   app.register_blueprint(write_review_bp) 
   app.register_blueprint(review_bp) 
   
   print(app.url_map)
   return app

#app = create_app()
#app.run()