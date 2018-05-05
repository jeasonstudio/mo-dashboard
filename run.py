from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
from flask_cors import CORS
from xmnlp import XmNLP
import requests

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

app = Flask(__name__, static_url_path='')
CORS(app)
api = Api(app)

class Sentiment(Resource):
  def get(self, text):
    xm = XmNLP(text)
    time_stamp = str(int(time.time()))
    data = get_tc_res(text, time_stamp)

    result = { 'polar': 0, 'confd': 0, 'sentiment': 0 }
    result['sentiment'] = xm.sentiment()
    result['polar'] = data['polar']
    result['confd'] = data['confd']
    return jsonify(result)

@app.route('/')
def index():
  return app.send_static_file('index.html')

api.add_resource(Sentiment, '/query/<text>')

if __name__ == '__main__':
  app.run(port='5002')

'''
GET /query/:text
response:
{
  polar: Int, // -1,0,1
  confd: Float, // 置信度
  sentiment: Float // 情感极性
}
'''
