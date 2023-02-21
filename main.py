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
  url = "https://restapi.amap.com/v3/weather/weatherInfo"
  key = '1e1ec6319425c04e027d558b6f934317'
  data = {'key': key, "city": 442000}
  res = requests.post(url, data)
  resp_id = res.json()
  weather = resp_id["lives"][0]

  umbrella = weather["weather"]
  if umbrella == "晴":
    msg = "天气好像不错诶，会有小太阳吧，会是暖暖的一天哦"
  if umbrella == "阴":
    msg = "太阳去玩躲猫猫了，好像有点冷诶"
  if umbrella == "多云":
    msg = "呀，好多云啊，一朵，两朵,三..."
  a = '雨'
  b = umbrella
  a_set = set(a)
  b_set = set(b)
  if len(a_set & b_set) > 0:
    msg = "看来今天小太阳下班了啊"
    msg1 = "好像下雨了要，记得把雨伞带好哦，别被淋湿了哦"
  else:
    msg1 = "那个有人告诉我今天不下雨，但是怕万一，所以你要看一下外面在看看要不要带雨伞哦"

  return weather['weather'], weather['temperature'], msg, msg1

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
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":msg1},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
