def GetWeather(city):
  import requests

  url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=16d123a52e5c07ef13e101ad033248ea&units=metric'.format(city)

  res = requests.get(url) # type: ignore
  data = res.json()
  
  GetWeather.temp = data['main']['temp']
  GetWeather.temp = (GetWeather.temp * 9/5) + 32
  GetWeather.wind = data['wind']['speed']
  GetWeather.desc = data['weather'][0]['description']
  GetWeather.humidity = data['main']['humidity']
