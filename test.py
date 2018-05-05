import requests

valueText = '今天天气不错啊'

from urllib.parse import quote
import time
from hashlib import md5
import json

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def get_tc_res(valueText, time_stamp):
  host = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar'
  APP_ID = '1106884428'
  APP_KEY = 'jCTZ5uhKuSv3gkR8'
  nonce_str = 'fa577ce340859f9fe'
  text = quote(valueText)
  str = 'app_id=' + APP_ID + '&nonce_str=' + nonce_str + '&text=' + text + '&time_stamp=' + time_stamp 
  sig = make_md5(str + '&app_key=' + APP_KEY, encoding='utf-8').upper()

  request = requests.session()
  req = request.get(host + '?sign=' + sig + '&' + str)
  return json.loads(req.text)['data']

time_stamp = str(int(time.time()))
get_tc_res(valueText, time_stamp)