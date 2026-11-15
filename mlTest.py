#dictonary  then editing it then calculation the temp acc to it
weather_dict = {"temp": 20,
              "humidity": 25,
              "wind speed": 30}
weather_dict["temp"] = float(
    input("Enter the current temperature(in degree celsius): ")
)
weather_dict["humidity"] = float(
    input("Enter the current humidity: ")
)
weather_dict["wind speed"] = float(
    input("Enter the current wind speed(in km/h): ")
)

if weather_dict["temp"] < 0:
    print("The temperature is below freezing point.")

elif weather_dict["temp"] >= 0 and weather_dict["temp"] <= 20 and weather_dict["humidity"] > 50:
    print("The weather is cool and humid.")

elif weather_dict["temp"] >= 0 and weather_dict["temp"] <= 20 and weather_dict["humidity"] <= 50:
    print("The weather is cool and dry.")

elif weather_dict["temp"] > 20 and weather_dict["temp"] <= 30 and weather_dict["humidity"] > 50:    
    print("The weather is warm and humid.")

elif weather_dict["temp"] > 20 and weather_dict["temp"] <= 30 and weather_dict["humidity"] <= 50:
    print("The weather is warm and dry.")

elif weather_dict["temp"] > 30 and weather_dict["humidity"] > 50:
    print("The weather is hot and humid.")                                  

elif weather_dict["temp"] > 30 and weather_dict["humidity"] <= 50:
    print("The weather is hot and dry.")

elif weather_dict["temp"] > 40:
    print("The temperature is above 40 degrees Celsius. It's extremely hot!")

elif weather_dict["temp"] < -10:
    print("The temperature is below -10 degrees Celsius. It's extremely cold!")

elif weather_dict["temp"] >= 100:
    print("Bro!! u on mars or what!?")       


#Wind Speed Ranges (Beaufort Scale & General Classification)

#• Calm: 0 – 1 km/h (0 mph) — Smoke rises straight up.
#• Light Air / Breeze: 1 – 19 km/h (1 – 12 mph) — Leaves rustle, wind felt on face.
#• Moderate to Fresh Breeze: 20 – 38 km/h (13 – 24 mph) — Small branches move, dust/paper raised.
#• Strong Breeze / Near Gale: 39 – 61 km/h (24 – 38 mph) — Large tree branches sway, hard to use an umbrella.
#• Gale to Storm: 62 – 102+ km/h (39 – 63+ mph) — Twigs/branches break, walking is difficult, trees can be uprooted.
#• Local Context (Kolkata/West Bengal): Average wind speeds generally hover around 2.6 m/s (approx. 9.4 km/h), peaking up to 10.4 m/s (approx. 37.5 km/h) during regular conditions.

#Relative Humidity Ranges

#• Dry Weather: 20% – 40% relative humidity — Air feels crisp or dry; low moisture capacity.
#• Normal / Comfortable Range: 30% – 50% relative humidity — Typical indoor/outdoor baseline.
#• Humid Weather: 60% – 80% relative humidity — Air feels noticeably damp or muggy.
#• Very High / Saturated: 80% – 100% relative humidity — Common during monsoons, rainy days, or early mornings; air holds near its maximum water-vapor capacity.

if weather_dict["wind speed"] < 1: 
    print("The wind is calm.")

elif weather_dict["wind speed"] >= 1 and weather_dict["wind speed"] <= 19:
    print("The wind is light air/breeze.")

elif weather_dict["wind speed"] >= 20 and weather_dict["wind speed"] <= 38:
    print("The wind is moderate to fresh breeze.")

elif weather_dict["wind speed"] >= 39 and weather_dict["wind speed"] <= 61:
    print("The wind is strong breeze/near gale.")

elif weather_dict["wind speed"] >= 62 and weather_dict["wind speed"] <= 102:
    print("The wind is gale to storm.")

