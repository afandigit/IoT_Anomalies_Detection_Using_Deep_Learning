from functions import *
from tensorflow import keras
import time


tcn_model = keras.models.load_model('./TCN_Model_rmse', custom_objects={'rmse': rmse})

while True:

    #     get data from data base
    '''
    Here, we will query the database for the last 11 records collected by sensors in real-time. We fit the first 10 records to the model so 
    it can predict the 'humidity' and 'temperature' values for the next timestamp. Then, we verify the 11th record against the predicted 
    values ('humidity' and 'temperature') to determine if it is an anomalous value or not.
    '''
    X = get_last_11_data_records()

    #   Detect the anomaly
    pred = is_anomalie(tcn_model, X[:10], X[10])

    #   send SMS
    phone_number = "+2126xxxxxxxx"
    Send_SMS(phone_number , pred)
    
    time.sleep(60)
