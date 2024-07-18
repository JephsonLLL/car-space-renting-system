import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from backend.auto_tasks import * 

from apps import create_app 
#from celery import Celery 
from datetime import timedelta 

app = create_app() 
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config) 


# def start_update_price(): 
#     auto_update_price.apply_async(countdown=timedelta(days=1).seconds)
    
# def start_update_booking_status():
#     auto_update_booking_status.apply_async(countdown=timedelta(days=1).seconds)

if __name__ == '__main__': 
    # start_update_price() 
    # start_update_booking_status() 
    #app.run(debug=True)
    app.run()
