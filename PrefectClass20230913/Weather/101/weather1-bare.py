import httpx
from prefect import Flow, Task

@Flow
def fetch_weather(lat: float, lon: float):
    some_temp = get_temperature(lat, lon)
    print(f'Some temperature = {some_temp}')
    some_windspeed = get_windspeed(lat, lon)
    return sum(some_temp, some_windspeed)

@Task
def get_temperature(lat, lon): 
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    # print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp

@Task
def get_windspeed(lat, lon): 
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m"),
    )
    # print(weather.json())
    most_recent_windspeed = float(weather.json()["hourly"]["windspeed_10m"][0])
    # print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_windspeed
@Task 
def sum(a,b): 
    return a+b

if __name__ == "__main__":
    fetch_weather.serve(name = 'test-flow')
    # fetch_weather(30,60)
    # (38.9, -77.0)