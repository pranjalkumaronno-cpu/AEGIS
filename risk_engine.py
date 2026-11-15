
# AEGIS - Risk Intelligence Engine
# Version 1.0

def analyze_weather(weather):

    temperature = weather["temperature_2m"]
    wind_speed = weather["wind_speed_10m"]
    precipitation = weather["precipitation"]
    weather_code = weather["weather_code"]

    risks = []

    # 1. Temperature analysis

    if temperature >= 45:
        risks.append({
            "type": "Extreme Heat",
            "level": "CRITICAL",
            "score": 3,
            "recommendation": "Avoid prolonged outdoor activity and follow local heat advisories."
        })

    elif temperature >= 40:
        risks.append({
            "type": "High Temperature",
            "level": "HIGH",
            "score": 2,
            "recommendation": "Stay hydrated and reduce strenuous outdoor activity."
        })

    elif temperature >= 35:
        risks.append({
            "type": "Heat Stress",
            "level": "MODERATE",
            "score": 1,
            "recommendation": "Stay hydrated and take breaks in shaded areas."
        })

    # 2. Wind analysis

    if wind_speed >= 62:
        risks.append({
            "type": "Extreme Wind",
            "level": "CRITICAL",
            "score": 3,
            "recommendation": "Seek shelter and follow official severe-weather guidance."
        })

    elif wind_speed >= 39 and wind_speed < 62:
        risks.append({
            "type": "Strong Wind",
            "level": "HIGH",
            "score": 2,
            "recommendation": "Secure loose outdoor objects and avoid exposed areas."
        })

    elif wind_speed >= 20 and wind_speed < 39:
        risks.append({
            "type": "Elevated Wind",
            "level": "MODERATE",
            "score": 1,
            "recommendation": "Exercise caution around trees and unsecured objects."
        })

    elif wind_speed >= 2 and wind_speed < 20:    
        risks.append({
            "type": "Light Wind",
            "level": "LOW",
            "score": 0,
            "recommendation": "Normal outdoor activities can proceed with caution."
        })
        
    elif wind_speed < 2:
        risks.append({
            "type": "Calm Wind",
            "level": "LOW",
            "score": 0,
            "recommendation": "Normal outdoor activities can proceed."
        })     

    # 3. Precipitation analysis

    if precipitation >= 15:
        risks.append({
            "type": "Heavy Current Precipitation",
            "level": "HIGH",
            "score": 2,
            "recommendation": "Monitor official rainfall and flood advisories."
        })

    elif precipitation >= 7:
        risks.append({
            "type": "Elevated Current Precipitation",
            "level": "MODERATE",
            "score": 1,
            "recommendation": "Monitor local rainfall conditions."
        })

    # 4. Thunderstorm detection

    if weather_code in [95, 96, 99]:
        risks.append({
            "type": "Thunderstorm",
            "level": "HIGH",
            "score": 2,
            "recommendation": "Move indoors and follow official weather alerts."
        })

    # 5. Calculate overall indicator

    if not risks:
        overall_level = "LOW"
        overall_score = 0

    else:
        overall_score = max(risk["score"] for risk in risks)

        levels = {
            0: "LOW",
            1: "MODERATE",
            2: "HIGH",
            3: "CRITICAL"
        }

        overall_level = levels[overall_score]

    return {
        "engine": "AEGIS Risk Engine",
        "version": "1.0",
        "overall_level": overall_level,
        "risk_score": overall_score,
        "identified_risks": risks,
        "risk_count": len(risks),
        "assessment_type": "Rule-based weather screening",
        "warning": (
            "This is an experimental weather indicator, "
            "not an official disaster warning or flood prediction."
        )
    }

