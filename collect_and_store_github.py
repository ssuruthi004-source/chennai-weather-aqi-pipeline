"""
GitHub Actions version: fetch Chennai weather + air quality data,
then INSERT it into Supabase. API key and DB connection string are
read from environment variables (set as GitHub Secrets), NOT
hardcoded, since this file lives in a public repository.
"""

import os
import requests
import psycopg2
from datetime import datetime, timezone

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")

LATITUDE = 13.0827
LONGITUDE = 80.2707
CITY = "Chennai"

now = datetime.now(timezone.utc)
reading_date = now.date()
reading_time = now

weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,weather_code",
}
weather_response = requests.get(weather_url, params=weather_params)
weather_data = weather_response.json()["current"]

print("Weather data fetched:", weather_data)

aqi_url = "http://api.openweathermap.org/data/2.5/air_pollution"
aqi_params = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": OPENWEATHER_API_KEY,
}
aqi_response = requests.get(aqi_url, params=aqi_params)
aqi_reading = aqi_response.json()["list"][0]
aqi_value = aqi_reading["main"]["aqi"]
components = aqi_reading["components"]

print("Air quality data fetched:", aqi_reading)

conn = psycopg2.connect(DB_CONNECTION_STRING)
cur = conn.cursor()

cur.execute(
    """
    INSERT INTO weather_readings
        (city, reading_date, reading_time, temperature_c, humidity_pct, wind_speed_kmh, pressure_hpa, weather_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (
        CITY,
        reading_date,
        reading_time,
        weather_data["temperature_2m"],
        weather_data["relative_humidity_2m"],
        weather_data["wind_speed_10m"],
        weather_data["surface_pressure"],
        weather_data["weather_code"],
    ),
)

cur.execute(
    """
    INSERT INTO air_quality_readings
        (city, reading_date, reading_time, aqi, pm2_5, pm10, no2, so2, co, o3)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (
        CITY,
        reading_date,
        reading_time,
        aqi_value,
        components["pm2_5"],
        components["pm10"],
        components["no2"],
        components["so2"],
        components["co"],
        components["o3"],
    ),
)

conn.commit()
cur.close()
conn.close()

print("\nSuccess! Both readings were inserted into Supabase.")
