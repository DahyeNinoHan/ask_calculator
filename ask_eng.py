import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# -------------------- Load Airport Data --------------------
@st.cache_data
def load_airport_data():
    url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
    cols = ['AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude',
            'Altitude', 'Timezone', 'DST', 'TzDatabaseTimeZone', 'Type', 'Source']
    df = pd.read_csv(url, header=None, names=cols)
    return df


df_airports = load_airport_data()


# -------------------- Haversine Formula --------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# -------------------- Get Coordinates --------------------
def get_coordinates(iata):
    result = df_airports[df_airports['IATA'] == iata.upper()]
    if not result.empty:
        return result.iloc[0]['Latitude'], result.iloc[0]['Longitude']
    return None, None

# -------------------- Streamlit UI --------------------
st.title("ASK Calculator")
st.markdown("Enter the IATA codes, number of available seats per flight, and weekly frequency to calculate the distance, annual seat supply, and ASK.")

col1, col2 = st.columns(2)
with col1:
    orig = st.text_input("Origin Airport IATA Code (e.g., ICN)")
with col2:
    dest = st.text_input("Destination Airport IATA Code (e.g., LAX)")


available_seats = st.number_input("Available Seats per Flight", min_value=1, value=300)
frequency = st.number_input("Weekly Frequency", min_value=1, value=7)

if st.button("Calculate"):
    lat1, lon1 = get_coordinates(orig)
    lat2, lon2 = get_coordinates(dest)

    if None in (lat1, lon1, lat2, lon2):
        st.error("⚠️ Invalid IATA code(s). Please check your input.")

    else:
        distance = haversine(lat1, lon1, lat2, lon2)
        weekly_seats = available_seats * frequency
        annual_seats = weekly_seats * 52
        ask = annual_seats * distance

        st.success(f"🛫 **Route: {orig.upper()} → {dest.upper()}**")
        st.write(f"**📏 Distance:** {distance:,.2f} km")
        st.write(f"**💺 Weekly Seats:** {weekly_seats:,}")
        st.write(f"**📆 Annual Seats:** {annual_seats:,}")
        st.write(f"**📊 ASK (Available Seat Kilometers):** {ask:,.0f} km")
