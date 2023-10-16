import requests
import os
import json
import datetime


def getApi(latitude = 52.2297,longitude = 21.0122):
    searched_date = input("Podaj date(YYYY-mm-dd): ")
    if not searched_date:
        date = datetime.date.today() + datetime.timedelta(days=1)
        searched_date = date.strftime("%Y-%m-%d")

    data_path = "weather.json"
    if os.path.exists(data_path):
        with open(data_path) as file:
            for line in file:
                data = json.loads(line)
                if searched_date in data["daily"]["time"][0]:
                    if "rain_sum" in data["daily"]:
                        value = data["daily"]["rain_sum"][0]
                        return value

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rain_sum = data["daily"]["rain_sum"]
        with open(data_path, 'a') as file:
            file.write(json.dumps(data)+"\n")
            if "rain_sum" in data["daily"]:
                value = data["daily"]["rain_sum"][0]
    else:
        value = -1

    return value

def readApi(rain_sum):
    if rain_sum == 0.0:
        print("Nie bedzie padac.")
    if rain_sum > 0.0:
        print("Bedzie padac")
    if rain_sum < 0.0:
        print("Nie wiem")

def main():
    print("Prognoza pogody dla Warszawy.")
    rain_sum = getApi()
    readApi(rain_sum)

if __name__ == "__main__":
    main()