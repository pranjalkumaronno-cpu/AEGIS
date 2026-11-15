
from fastapi import FastAPI, HTTPException
import requests

from risk_engine import analyze_weather


app = FastAPI(
    title="AEGIS API",
    description="Global Weather and Crisis Intelligence",
    version="1.1"
)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# HOME
@app.get("/")
def home():
    return {
        "project": "AEGIS",
        "message": "Backend is running!",
        "status": "ONLINE"
    }


# HEALTH
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AEGIS Backend"
    }


# ABOUT
@app.get("/about")
def about():
    return {
        "project": "AEGIS",
        "project_type": "AI-powered crisis intelligence",
        "developer_role": "Backend developer",
        "status": "In development"
    }


# WEATHER CONDITION TRANSLATOR
def describe_weather(code):

    conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }

    return conditions.get(code, "Unknown weather condition")


# WEATHER ENDPOINT
@app.get("/weather/{city}")
def get_weather(city: str, units: str = "celsius"):

    allowed_units = ["celsius", "fahrenheit", "kelvin"]

    units = units.lower()

    if units not in allowed_units:
        raise HTTPException(
            status_code=400,
            detail="Invalid unit. Use celsius, fahrenheit, or kelvin."
        )

    city = city.strip()

    if not city or city.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid city name."
        )

    try:
        # STEP 1: Find city coordinates

        location_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        location_response.raise_for_status()

        location_data = location_response.json()
        results = location_data.get("results", [])

        if not results:
            raise HTTPException(
                status_code=404,
                detail="City not found."
            )

        location = results[0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # STEP 2: Fetch current weather

        temperature_unit = (
            "fahrenheit" if units == "fahrenheit" else "celsius"
        )

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m,"
                    "wind_direction_10m"
                ),
                "temperature_unit": temperature_unit,
                "wind_speed_unit": "kmh",
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data["current"]

        temperature = current["temperature_2m"]

        # STEP 3: Convert to Kelvin if requested

        if units == "kelvin":
            temperature = round(temperature + 273.15, 2)

        # STEP 4: Build weather report

        weather_code = current["weather_code"]

        return {
            "project": "AEGIS",
            "location": {
                "city": location["name"],
                "country": location.get("country"),
                "latitude": latitude,
                "longitude": longitude
            },
            "weather": {
                "temperature": temperature,
                "units": units,
                "humidity": current["relative_humidity_2m"],
                "apparent_temperature": current["apparent_temperature"],
                "precipitation": current["precipitation"],
                "wind_speed_kmh": current["wind_speed_10m"],
                "wind_direction_degrees": current["wind_direction_10m"],
                "condition": describe_weather(weather_code),
                "weather_code": weather_code,
                "observation_time": current["time"]
            },
            "data_source": "Open-Meteo",
            "data_type": "Model-based current weather conditions",
            "status": "SUCCESS"
        }

    except HTTPException:
        raise

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Weather service is currently unavailable."
        )

    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="Unexpected response received from weather service."
        )


# RISK ENDPOINT
@app.get("/risk/{city}")
def get_risk(city: str):

    city = city.strip()

    if not city or city.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid city name."
        )

    try:
        # STEP 1: Find city coordinates

        location_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        location_response.raise_for_status()

        results = location_response.json().get("results", [])

        if not results:
            raise HTTPException(
                status_code=404,
                detail="City not found."
            )

        location = results[0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # STEP 2: Fetch weather in Celsius

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "temperature_unit": "celsius",
                "wind_speed_unit": "kmh",
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()

        current = weather_response.json()["current"]

        # STEP 3: Run AEGIS Risk Engine

        risk_result = analyze_weather(current)

        # STEP 4: Return intelligence report

        return {
            "project": "AEGIS",
            "location": {
                "city": location["name"],
                "country": location.get("country"),
                "latitude": latitude,
                "longitude": longitude
            },
            "weather_data": {
                "temperature_celsius": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "wind_speed_kmh": current["wind_speed_10m"],
                "precipitation": current["precipitation"],
                "weather_code": current["weather_code"],
                "observation_time": current["time"]
            },
            "intelligence": risk_result,
            "status": "SUCCESS"
        }

    except HTTPException:
        raise

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable."
        )

    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="Invalid weather data received."
        )


# GREET
@app.get("/greet/{name}")
def greet(name: str, language: str = "English"):

    if len(name.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Name must be at least 2 characters long."
        )

    return {
        "name": name,
        "language": language,
        "message": f"Hello {name}!"
    }
