def WeatherPlug(city):
  import requests

  url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=16d123a52e5c07ef13e101ad033248ea&units=metric'.format(city)

  res = requests.get(url) # type: ignore
  data = res.json()
  
  WeatherPlug.temp = data['main']['temp']
  WeatherPlug.temp = (WeatherPlug.temp * 9/5) + 32
  WeatherPlug.wind = data['wind']['speed']
  WeatherPlug.desc = data['weather'][0]['description']
  WeatherPlug.humidity = data['main']['humidity']
