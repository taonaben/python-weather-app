import requests

api_key = "6f9d8bafe385355540becf1debce589d"


def get_weather_data(city):
    """
    Make a GET request to the OpenWeatherMap API for the given city name, and
    return the JSON response as a Python dictionary.

    Parameters
    ----------
    city : str
        The name of the city for which to retrieve weather data.

    Returns
    -------
    dict
        The JSON response from the OpenWeatherMap API as a Python dictionary.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}"
    response = requests.get(url)
    return response.json()


def display_weather_data(data):
    """
    Take a dictionary of weather data and print it in a human-readable format.

    Parameters
    ----------
    data : dict
        The dictionary of weather data returned from the OpenWeatherMap API.

    Returns
    -------
    None
    """

    if data["cod"] == "404":
        print("Error: City not found")
        return

    print(f"\n\nCity: {data['name']}")
    print(f"Temperature: {data['main']['temp']} °C")
    print(f"Feels like: {data['main']['feels_like']} °C")
    print(f"Minimum Temperature: {data['main']['temp_min']} °C")
    print(f"Maximum Temperature: {data['main']['temp_max']} °C")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Pressure: {data['main']['pressure']} hPa")
    print(f"Wind Speed: {data['wind']['speed']} m/s")
    print(f"Description: {data['weather'][0]['description']}")


def main():
    city = input("Enter a city name: ")
    data = get_weather_data(city)
    display_weather_data(data)


if __name__ == "__main__":
    main()
