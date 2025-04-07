import os
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Set page config
st.set_page_config(page_title="Weather App", page_icon="☁️", layout="centered")

# Use secrets or environment variables for API key
# In production, use st.secrets["OPENWEATHER_API_KEY"]
# For development, you can set environment variables or use a .env file with python-dotenv
load_dotenv()  # take environment variables from .env
api_key = os.environ.get("OPENWEATHER_API_KEY")

# Add a title and description
st.title("☁️ Weather Dashboard")
st.write("Get current weather information for any city around the world.")


@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_weather_data(city):
    """
    Make a GET request to the OpenWeatherMap API for the given city name

    Parameters
    ----------
    city : str
        The name of the city for which to retrieve weather data.

    Returns
    -------
    dict
        The JSON response from the OpenWeatherMap API as a Python dictionary.
    """
    if not city:  # Return None if city is empty
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None


def display_weather_data(data):
    """
    Display weather data in a formatted Streamlit UI

    Parameters
    ----------
    data : dict
        The dictionary of weather data returned from the OpenWeatherMap API.
    """
    if data is None:
        return

    if data.get("cod") == "404":
        st.error("City not found. Please check the spelling and try again.")
        return

    # Get timestamp and convert to readable date/time
    timestamp = data.get("dt", 0)
    date_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    # Display city name and country
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(f"{data['name']}, {data['sys']['country']}")
    with col2:
        # Display weather icon
        if "weather" in data and len(data["weather"]) > 0:
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            st.image(icon_url, width=100)

    st.write(f"Last Updated: {date_time}")

    # Main weather info
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Temperature", f"{data['main']['temp']}°C")
        st.metric("Feels Like", f"{data['main']['feels_like']}°C")
        st.metric("Humidity", f"{data['main']['humidity']}%")

    with col2:
        st.metric("Wind Speed", f"{data['wind']['speed']} m/s")
        st.metric("Pressure", f"{data['main']['pressure']} hPa")
        if "weather" in data and len(data["weather"]) > 0:
            st.write(
                f"**Description**: {data['weather'][0]['description'].capitalize()}"
            )

    # Additional weather data in an expander
    with st.expander("Additional Details"):
        st.write(f"**Min Temperature**: {data['main']['temp_min']}°C")
        st.write(f"**Max Temperature**: {data['main']['temp_max']}°C")

        if "visibility" in data:
            visibility_km = data["visibility"] / 1000
            st.write(f"**Visibility**: {visibility_km:.1f} km")

        if "clouds" in data:
            st.write(f"**Cloudiness**: {data['clouds'].get('all', 0)}%")

        if "rain" in data:
            st.write(f"**Rain (1h)**: {data['rain'].get('1h', 0)} mm")

        if "snow" in data:
            st.write(f"**Snow (1h)**: {data['snow'].get('1h', 0)} mm")

        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
        st.write(f"**Sunrise**: {sunrise}")
        st.write(f"**Sunset**: {sunset}")


def main():
    # City search box
    city = st.text_input("Enter a city name:", key="city_input")

    # Search button
    search_col, clear_col = st.columns([1, 5])
    with search_col:
        search = st.button("Search")

    # If search button is clicked or Enter is pressed in the text input
    if search and city:
        with st.spinner("Fetching weather data..."):
            data = get_weather_data(city)
            display_weather_data(data)

    # Show some helpful information when no city is entered
    if not city:
        st.info("Enter a city name to get started!")


if __name__ == "__main__":
    main()
