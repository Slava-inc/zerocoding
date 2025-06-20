from my_token import TOKEN
import requests as rq

# city = "Moscow"
city = input("Введите город: ")
# url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={TOKEN}"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={TOKEN}&units=metric&lang=ru"

response = rq.get(url)
print(response.status_code)
print(response.text)

data = response.json()
print(data)
if response.status_code == 200:
    print(f"Погода в городе {city}")
    # print(f"🌡 Температура: {round(data['main']['temp']-273.15, 1)} °C") # alt 01456 - символ градуса
    print(f"🌡 Температура: {data['main']['temp']} °C") # alt 01456 - символ градуса
    print(f"🌡 Погода: {data['weather'][0]['description']}")
    print(f"🌡Влажность: {data['main']['humidity']} %")