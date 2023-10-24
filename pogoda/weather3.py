import os
import json
import requests
import datetime


class WeatherForecast:
    def __init__(self):
        self.data = {}

        if os.path.exists("weather.json"):
            with open("weather.json") as file:
                self.data = json.load(file)

    def __setitem__(self, date, forecast):
        self.data[date] = forecast
        with open("weather.json", "w") as file:
            json.dump(self.data, file, indent=2)

    def __getitem__(self, date):
        if date in self.data:
            return self.data[date]
        else:
            return self.get_data(date)

    def items(self):
        for date, forecast in self.data.items():
            yield date, forecast

    def __iter__(self):
        return iter(self.data)

    def get_data(self, date):
        latitude = 51.1079
        longitude = 17.0385
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            result = data["daily"]["rain_sum"][0]
            forecast = "Bedzie padac" if result > 0.0 else "Nie bedzie padac"
            self[date] = forecast
            return forecast
        else:
            return "Nie wiem"


if __name__ == "__main__":
    weather_forecast = WeatherForecast()
    searched_date = input("Podaj date (YYYY-mm-dd): ")
    if not searched_date:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        searched_date = tomorrow.strftime("%Y-%m-%d")

    result = weather_forecast[searched_date]
    print("Pogoda dla Wroclawia")
    print(f"Prognoza pogody na dzien {searched_date} to {result}")

    for date in weather_forecast:
        forecast = weather_forecast[date]
        print(f"{date}: {forecast}")
