
# AEGIS - Weather Analysis Engine
# Day 1

from sympy import python


weather = {
    "city": "Kolkata",
    "temperature": 39,
    "humidity": 85,
    "wind_speed": 25
}


def analyze_weather(data):

    city = data["city"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]


    if temperature >= 40:
        status = "EXTREME HEAT"
    elif temperature >= 35:
        status = "HIGH HEAT"
    else:
        status = "NORMAL"

    if(humidity > 90):
        statusH = "HIGH HUMIDITY"
    else:
        statusH = "NORMAL HUMIDITY"

    result = {
        "location": city,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "status": status,
        "humidity_status": statusH
    }

    return result


analysis = analyze_weather(weather)

print("===== AEGIS WEATHER REPORT =====")

for key, value in analysis.items():
    print(f"{key}: {value}")
    