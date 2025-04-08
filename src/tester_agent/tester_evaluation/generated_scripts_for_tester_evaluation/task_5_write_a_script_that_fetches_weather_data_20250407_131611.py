import requests
import csv

API_KEY = "your_api_key"
CITY = "London"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

response = requests.get(URL)

if response.status_code != 200:
    print("Error fetching weather data")
    exit()

weather_data = response.json()

with open('weather_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["City", "Temperature (C)", "Humidity (%)"])
    writer.writerow([weather_data['name'], weather_data['main']['temp'], weather_data['main']['humidity']])

print("Weather data saved to weather_data.csv")