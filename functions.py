from twilio.rest import Client
import pymysql
import pandas as pd
import keras.backend as K
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------------------------------------------------------------------

def rmse(y_true, y_pred):
    """
    Calculates the root mean square error (RMSE) between the real and predicted values.
    """
    return K.sqrt(K.mean(K.square(y_pred - y_true)))



# ---------------------------------------------------------------------------------------------------------------------

def is_anomalie(model, sensors_real_time_data, next_timestep_current_data):

    """
    This function detects anomalies by comparing model predictions to current values (real data).
    """

    # Reshape the new current data (real data) from the sensors to fit the model.
    sensors_real_time_data = sensors_real_time_data.reshape(-1, 10, 2)





    # Calculate the standard deviations of the humidity and temperature of the new current data (real data) from the sensors.
    Humidity_std = sensors_real_time_data[:,0].std()
    temperature_std = sensors_real_time_data[:,1].std()





    # Makes a prediction of humidity and temperature values for the next time step.
    pred = model.predict(sensors_real_time_data)





    # Get the temperature prediction for the single value
    Humidity_prediction = pred[0][0]
    Temperature_prediction = pred[0][1]




    # Compares predicted values to real values to determine if there are anomalies
    Not_Humidity_anomaly = Humidity_prediction - 3 * (Humidity_std+ 0.01)< next_timestep_current_data[0]< Humidity_prediction + 3 * (Humidity_std+ 0.01)
    Not_Temperature_anomaly = Temperature_prediction - 3 *(temperature_std + 0.01)< next_timestep_current_data[1]< Temperature_prediction + 3 * (temperature_std + 0.01)
    



    """
    Returns a tuple indicating if there is a humidity and/or temperature anomaly in a sensor (0 = no anomaly, 1 = anomaly)
    """
    return (int(not Not_Humidity_anomaly), int(not Not_Temperature_anomaly))



# ---------------------------------------------------------------------------------------------------------------------

def Send_SMS(phone_number , pred):
    """
    This function sends an SMS if an anomaly is detected or not.
    """

    if (phone_number.startswith('0')) :
        phone_number = "+212"+phone_number[1:]

    temp = ''
    hum = ''

    if(pred[0]):
        temp = "Temperature Sensor"
    if(pred[1]):
        hum = "Humidity Sensor"

    if pred[0] or pred[1]:
        account_sid = ""
        auth_token = ""

        # Uses the Twilio API to send an SMS
        client = Client(account_sid, auth_token)
        



        
        # Formats the alert message based on detected anomalies (temperature and/or humidity)
        client.messages.create(
            body="Salam :), there is an anomaly in the sensor : "+temp +' - '+hum+".",
            from_="+... .. .. .. ..",
            to=phone_number
        )



# ---------------------------------------------------------------------------------------------------------------------

def get_last_11_data_records():
    
    '''
    Here, we will query the database for the last 11 records collected by sensors in real-time. We fit the first 10 records to the model so 
    it can predict the 'humidity' and 'temperature' values for the next timestamp. Then, we verify the 11th record against the predicted 
    values ('humidity' and 'temperature') to determine if it is an anomalous value or not.
    '''

    connection = pymysql.connect(host='localhost',user='root',password='', db='sensors_data' , port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `sensors` ORDER by time DESC limit 11;")
    rows = cursor.fetchall()
    rows = reversed(rows)

    df = pd.DataFrame(rows)

    cursor.close()
    connection.close()

    scaler = StandardScaler()
    df = scaler.fit_transform(df[['humidity','temperature']])
    return df


