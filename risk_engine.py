
def analyze_weather(weather_data):

    required_fields = [
        "temperature_2m",
        "wind_speed_10m",
        "precipitation",
        "weather_code"
    ]

    for field in required_fields:
        if field not in weather_data or weather_data[field] is None:
            raise ValueError(f"Missing weather data: {field}")

    temperature = float(weather_data["temperature_2m"])
    wind_speed = float(weather_data["wind_speed_10m"])
    precipitation = float(weather_data["precipitation"])
    weather_code = int(weather_data["weather_code"])

    if temperature < -100 or temperature > 70:
        raise ValueError("Invalid temperature value.")

    if wind_speed < 0 or wind_speed > 500:
        raise ValueError("Invalid wind speed.")

    if precipitation < 0:
        raise ValueError("Invalid precipitation value.")

    identified_risks = []

    if temperature >= 45:
        identified_risks.append({
            "type": "Extreme Heat",
            "level": "CRITICAL",
            "score": 3,
            "observed_value": temperature,
            "unit": "°C",
            "recommendation": "Avoid prolonged outdoor activity and follow official heat advisories."
        })

    elif temperature >= 40:
        identified_risks.append({
            "type": "High Temperature",
            "level": "HIGH",
            "score": 2,
            "observed_value": temperature,
            "unit": "°C",
            "recommendation": "Stay hydrated and reduce strenuous outdoor activity."
        })

    elif temperature >= 35:
        identified_risks.append({
            "type": "Heat Stress",
            "level": "MODERATE",
            "score": 1,
            "observed_value": temperature,
            "unit": "°C",
            "recommendation": "Stay hydrated and take breaks in shaded areas."
        })

    if wind_speed >= 62:
        identified_risks.append({
            "type": "Extreme Wind",
            "level": "CRITICAL",
            "score": 3,
            "observed_value": wind_speed,
            "unit": "km/h",
            "recommendation": "Seek appropriate shelter and follow official severe-weather guidance."
        })

    elif wind_speed >= 39:
        identified_risks.append({
            "type": "Strong Wind",
            "level": "HIGH",
            "score": 2,
            "observed_value": wind_speed,
            "unit": "km/h",
            "recommendation": "Secure loose outdoor objects and avoid exposed areas."
        })

    elif wind_speed >= 20:
        identified_risks.append({
            "type": "Elevated Wind",
            "level": "MODERATE",
            "score": 1,
            "observed_value": wind_speed,
            "unit": "km/h",
            "recommendation": "Exercise caution around trees and unsecured objects."
        })

    if precipitation >= 15:
        identified_risks.append({
            "type": "Heavy Current Precipitation",
            "level": "HIGH",
            "score": 2,
            "observed_value": precipitation,
            "unit": "mm",
            "recommendation": "Monitor official rainfall and flood advisories."
        })

    elif precipitation >= 7:
        identified_risks.append({
            "type": "Elevated Current Precipitation",
            "level": "MODERATE",
            "score": 1,
            "observed_value": precipitation,
            "unit": "mm",
            "recommendation": "Monitor local rainfall conditions."
        })

    if weather_code in [95, 96, 99]:
        identified_risks.append({
            "type": "Thunderstorm",
            "level": "HIGH",
            "score": 2,
            "observed_value": weather_code,
            "unit": "weather code",
            "recommendation": "Move indoors and follow official weather alerts."
        })

    if identified_risks:
        overall_score = max(
            risk["score"] for risk in identified_risks
        )
    else:
        overall_score = 0

    risk_levels = {
        0: "LOW",
        1: "MODERATE",
        2: "HIGH",
        3: "CRITICAL"
    }

    return {
        "engine": "AEGIS Risk Engine",
        "version": "2.0",
        "overall_level": risk_levels[overall_score],
        "risk_score": overall_score,
        "identified_risks": identified_risks,
        "risk_count": len(identified_risks),
        "assessment_type": "Rule-based weather screening",
        "scoring_method": "Highest individual risk score",
        "warning": (
            "This is an experimental weather screening indicator, "
            "not an official disaster warning or disaster prediction."
        )
    }
