import httpx  # requests capability, but can work with async
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact
from prefect.tasks import task_input_hash
@task(retries = 3, cache_key_fn=task_input_hash)
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    create_markdown_artifact(
        key = 'report',
        markdown = "#whoohoo",
        description = 'just a try to do something'
    )
    return most_recent_temp
@task
def save_weather(temp: float):
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"
@flow()
def pipeline(lat: float, lon: float):
    temp = fetch_weather(lat, lon)
    result = save_weather(temp)
    return result
if __name__ == "__main__":
    pipeline.serve(name='just-another-test')