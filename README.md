# Real-Time Anomaly Detection System

## Overview
This project is designed to monitor real-time humidity and temperature data captured by IoT sensors and detecting any abnormal behavior that could indicate a failure or intrusion into the system and sending SMS alerts if anomalies are detected. The project leverages a Temporal Convolutional Network (TCN) model to make predictions and identify anomalies.


## Features
- Real-time data monitoring
- Anomaly detection using a TCN model
- SMS alerts for detected anomalies
- Data standardization and preprocessing
- Continuous operation with periodic checks
- Data Preparation
- Explore and Visualize data - Time Serie Problem
- Train a Deep Learning model
- Communicate results

## Requirements
- Python 3.x
- TensorFlow
- Keras
- pymysql
- numpy
- pandas
- scikit-learn
- twilio

## Set up the database:

- Ensure you have a MySQL server running.
- Create a database named sensors_data.
- Create a table named sensors with columns for humidity, temperature, and time.

## Contribution
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
