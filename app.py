import streamlit as st
import requests

'''
# TaxiFareModel front
'''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')
'''
## Date and time
'''

import datetime

# d = st.date_input(
#     "Select a date",
#     datetime.date(2019, 7, 6))
# st.write('date:', d)

# t = st.time_input('time', datetime.time(8, 45))

# st.write('Alarm is set for', t)

d = st.date_input(
    "Which date do you want to select?",
    datetime.date(2019, 7, 6))


t = st.time_input('Select the time you would like for your ride', datetime.time(8, 45))

dt = datetime.datetime.combine(d,t)

st.write('Your ride is set for', dt)

'''
## Pickup longitude
'''
pickup_long = st.number_input('Insert pickup longitude')

st.write('Pickup longitude', pickup_long)

'''
## Pickup latitude
'''
pickup_lat = st.number_input('Insert pickup lattitude')

st.write('Pickup lattitude', pickup_lat)

'''
## Dropoff longitude
'''
dropoff_long = st.number_input('Insert dropoff longitude')

st.write('Dropoff longitude', dropoff_long)

'''
## Dropoff latitude
'''
dropoff_lat = st.number_input('Insert dropoff lattitude')

st.write('Dropoff lattitude', dropoff_lat)

'''
## Passenger count
'''
option = st.slider('Select number of passengers', 1, 10, 3)

# filtered_df = df[df['first column'] % option == 0]

st.write('Number of passengers :', option)

## Once we have these, let's call our API in order to retrieve a prediction

url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

params = {
          'pickup_datetime': dt,
          'pickup_longitude': pickup_long,
          'pickup_latitude' : pickup_lat,
          'dropoff_longitude': dropoff_long,
          'dropoff_latitude': dropoff_lat,
          'passenger_count': option
          }

# '''
# 3. Let's call our API using the `requests` package...
# '''
response = requests.get(url, params=params)
prediction = response.json()

'''
## Fare
'''
st.write(round(prediction.get('fare'),2), '$')


