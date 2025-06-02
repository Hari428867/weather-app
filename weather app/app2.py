from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = 'e40f463b3e7f4083adc124023250206'  # Use WeatherAPI key

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    astro = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&aqi=no&alerts=no"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            error = data["error"].get("message", "Error fetching data")
        else:
            current = data["current"]
            location = data["location"]
            forecast_day = data["forecast"]["forecastday"][0]
            astro_data = forecast_day["astro"]

            weather = {
                "city": location["name"],
                "region": location["region"],
                "country": location["country"],
                "temperature": current["temp_c"],
                "feelslike": current["feelslike_c"],
                "condition": current["condition"]["text"],
                "icon": current["condition"]["icon"],
                "humidity": current["humidity"],
                "wind_kph": current["wind_kph"],
                "wind_dir": current["wind_dir"],
                "is_day": current["is_day"],
                "sunrise": astro_data["sunrise"],
                "sunset": astro_data["sunset"],
                "moon_phase": astro_data["moon_phase"],
                "moon_illumination": astro_data["moon_illumination"],
            }

            # Optional: Include next 3 days forecast
            forecast = []
            for day in data["forecast"]["forecastday"]:
                forecast.append({
                    "date": day["date"],
                    "maxtemp_c": day["day"]["maxtemp_c"],
                    "mintemp_c": day["day"]["mintemp_c"],
                    "condition": day["day"]["condition"]["text"],
                    "icon": day["day"]["condition"]["icon"],
                    "chance_of_rain": day["day"]["daily_chance_of_rain"]
                })

    return render_template("index1.html", weather=weather, forecast=forecast, error=error)

if __name__ == "__main__":
    app.run(debug=True)
