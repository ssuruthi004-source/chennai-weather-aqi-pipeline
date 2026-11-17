# Chennai Weather & Air Quality Pipeline

An automated data pipeline that collects weather and air quality readings for Chennai every day, stores them in a cloud PostgreSQL database, and shows the trends in an interactive Power BI dashboard.

## Dashboard

![Dashboard overview](Weather%20analysis%20Dashboard.png)

## How it works

Open-Meteo and OpenWeatherMap APIs → Python script → Supabase (PostgreSQL) → Power BI dashboard

A GitHub Actions workflow runs the Python script automatically every day at 02:00 UTC (7:30 AM IST), so the data keeps growing without any manual work.

## Tech stack

| Layer | Tool |
|---|---|
| Weather data | Open-Meteo API |
| Air quality data | OpenWeatherMap Air Pollution API |
| Collection script | Python (requests, psycopg2) |
| Database | Supabase (PostgreSQL) with Row Level Security enabled |
| Automation | GitHub Actions (scheduled daily run) |
| Visualisation | Power BI Desktop |

## Data collected

- **Weather:** temperature (°C), humidity (%), wind speed (km/h), pressure (hPa), weather code
- **Air quality:** AQI (1 = Good, 5 = Very Poor), PM2.5, PM10, NO2, SO2, CO, O3

The data is stored in two tables, `weather_readings` and `air_quality_readings`. Each row has a `city` column, so more cities can be added later without changing the design.

## Dashboard features

- Overview page: temperature and AQI trend charts, latest temperature card, AQI gauge, pollutant breakdown chart and a date-range slicer
- Weather details page: humidity, PM2.5, wind speed and pressure trends

## Security

API keys and the database connection string are stored as GitHub Secrets and read as environment variables, so no credentials appear in the code.

## Challenges and fixes

- **Network compatibility:** the direct Supabase connection failed on an IPv4-only network, so I switched to the Session pooler connection.
- **Special characters in the database password:** the password had to be URL-encoded inside the connection string.
- **API timeouts:** two scheduled runs failed when the weather API timed out. I diagnosed the cause from the GitHub Actions logs. Adding a request timeout and retries is a planned improvement.

## Repository files

- `collect_and_store_github.py` – fetches both readings and inserts them into the database
- `requirements.txt` – Python dependencies
- `.github/workflows/daily_run.yml` – the daily schedule

## Possible next steps

- Add a request timeout and retries
- Schedule the dashboard refresh in the Power BI service
- Add more cities
- Add alerts when AQI reaches 4 or 5
