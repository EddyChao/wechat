from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.itboy.net/api/weather/city/" + city
  res = requests.get(url).json()
  weatherHigh = res['data']['forecast'][0].high
  weatherLow = res['data']['forecast'][0].low
  weatherSunrise = res['data']['forecast'][0].sunrise
  weatherSunset = res['data']['forecast'][0].sunset
  weatherFx = res['data']['forecast'][0].fx
  weatherFj = res['data']['forecast'][0].fj
  weatherType = res['data']['forecast'][0].type
  weatherNotice = res['data']['forecast'][0].notice
  quality = res['data'].quality
  shidu = res['data'].shidu
  pm25 = res['data'].pm25
  pm10 = res['data'].pm10
  wendu = res['data'].wendu
  return weatherHigh,weatherLow,weatherSunrise,weatherSunset,weatherFx,weatherFj,weatherType,weatherNotice,quality,shidu,pm25,pm10,wendu

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weatherHigh,weatherLow,weatherSunrise,weatherSunset,weatherFx,weatherFj,weatherType,weatherNotice,quality,shidu,pm25,pm10,wendu = get_weather()
data = {"weatherHigh":{"value":weatherHigh,"color":get_random_color()},"weatherLow":{"value":weatherLow,"color":get_random_color()},"weatherSunrise":{"value":weatherSunrise,"color":get_random_color()},"weatherSunset":{"value":weatherSunset,"color":get_random_color()},"weatherFx":{"value":weatherFx,"color":get_random_color()},"weatherFj":{"value":weatherFj,"color":get_random_color()},"weatherType":{"value":weatherType,"color":get_random_color()},"weatherNotice":{"value":weatherNotice,"color":get_random_color()},"quality":{"value":quality,"color":get_random_color()},"shidu":{"value":shidu,"color":get_random_color()},"pm25":{"value":pm25,"color":get_random_color()},"pm10":{"value":pm10,"color":get_random_color()},"wendu":{"value":wendu,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(),"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
