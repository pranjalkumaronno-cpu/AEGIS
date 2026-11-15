from risk_engine import analyze_weather

sample_weather = {
    "temperature_2m": 42,
    "wind_speed_10m": 65,
    "precipitation": 2,
    "weather_code": 3
}

result = analyze_weather(sample_weather)

print(result)
