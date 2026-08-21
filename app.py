import streamlit as st
import datetime
import requests
import pandas as pd
import pydeck as pdk

'''
# Taxifare
'''

d = st.date_input(
    "Which date do you want to select?",
    datetime.date(2019, 7, 6))

t = st.time_input('Select the time you would like for your ride', datetime.time(8, 45))

dt = datetime.datetime.combine(d, t)

st.write('Your ride is set for', dt)

"""
### Where are you going ?
"""

def get_coordinates(address):
    try:
        r = requests.get(
            "https://photon.komoot.io/api/",
            params={"q": address, "limit": 1},
            headers={"User-Agent": "taxifare-streamlit-app"},
            timeout=10
        )
        data = r.json()
        if data.get("features"):
            lon, lat = data["features"][0]["geometry"]["coordinates"]
            return lat, lon
    except Exception:
        pass
    return None, None

pickup_address = st.text_input("Pickup address")
dropoff_address = st.text_input("Dropoff address")

pick_lat, pick_long = get_coordinates(pickup_address) if pickup_address else (None, None)
drop_lat, drop_long = get_coordinates(dropoff_address) if dropoff_address else (None, None)

if pickup_address and pick_lat is None:
    st.warning("Adresse de départ introuvable")
if dropoff_address and drop_lat is None:
    st.warning("Adresse d'arrivée introuvable")

"""
### Passengers
"""

option = st.slider('Select the number of passengers', 1, 6, 1)

st.write("Number of passengers: ", option)

url = 'https://taxifare.lewagon.ai/predict'

'''
# Price
'''

if pick_lat and pick_long and drop_lat and drop_long:

    params = {
        "pickup_datetime": dt,
        "pickup_longitude": pick_long,
        "pickup_latitude": pick_lat,
        "dropoff_longitude": drop_long,
        "dropoff_latitude": drop_lat,
        "passenger_count": option
    }

    response = requests.get(url, params=params)
    prediction = response.json()

    st.write("Your estimated price is", round(prediction["fare"], 2), "$")

    '''
    # Your itinerary
    '''

    def get_route(pick_lat, pick_long, drop_lat, drop_long):
        osrm_url = f"http://router.project-osrm.org/route/v1/driving/{pick_long},{pick_lat};{drop_long},{drop_lat}"
        osrm_params = {"overview": "full", "geometries": "geojson"}
        r = requests.get(osrm_url, params=osrm_params, timeout=10)
        return r.json()["routes"][0]["geometry"]["coordinates"]  # liste de [lon, lat]

    try:
        route_coords = get_route(pick_lat, pick_long, drop_lat, drop_long)

        path_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": route_coords}],
            get_path="path",
            get_width=4,
            get_color=[230, 80, 60],
            width_min_pixels=3,
        )

        points_layer = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame({
                "lat": [pick_lat, drop_lat],
                "lon": [pick_long, drop_long],
            }),
            get_position=["lon", "lat"],
            get_color=[0, 100, 200],
            get_radius=80,
        )

        view_state = pdk.ViewState(
            latitude=(pick_lat + drop_lat) / 2,
            longitude=(pick_long + drop_long) / 2,
            zoom=12,
        )

        st.pydeck_chart(pdk.Deck(
            layers=[path_layer, points_layer],
            initial_view_state=view_state,
            map_style="road"
        ))

    except Exception:
        st.warning("Impossible de calculer l'itinéraire routier pour le moment")

else:
    st.write("Merci de renseigner une adresse de départ et d'arrivée valides.")
