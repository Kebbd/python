import os
import json
import requests
import datetime

class WeatherForecast:
    def __init__(self):
        self.latitude = 51.1079
        self.longitude = 17.0385
        self.data = {}

        if os.path.exists("weather.json"):
            with open ("weather.json") as file:
                self.data = json.load(file)

    def __setitem__(self, set_date, forecast):
        self.data[set_date] = forecast
        with open('weather.json', 'w') as file:
            json.dump(self.data, file, indent=2)

    def __getitem__(self, get_date):
        return self.data.get(get_date, "Nie wiem")

    def items(self):
        for date, forecast in self.data.items():
            yield date, forecast

    def __iter__(self):
        return self.data


    def get_data(self, date):
        if date in self.data:
            return self.data[date]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"
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

    print(weather_forecast)
    print("Pogoda dla Wroclawia")
    result = weather_forecast.get_data(searched_date)
    weather_forecast[searched_date] = result
    forecast = weather_forecast[searched_date]
    print(f"Prognoza pogody na dzien {searched_date} to {forecast}")

    for date, forecast in weather_forecast.items():
        print(f"{date}: {forecast}")