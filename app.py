#!/bin/env python
# coding: utf-8

import os
import json
from flask import Flask, render_template, request, jsonify
import requests

from collections import OrderedDict
from operator import itemgetter


app = Flask(__name__)
app.debug = True

channel_access_token = os.environ['Channel_Access_Token']

def reply_message(replyToken, text):
    req_header = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(channel_access_token)
    }

    text_object = {
        'type': "text",
        'text': text
    }
    req_body = {
        'replyToken': replyToken,
        'messages': [
            text_object
        ]
    }
    r = requests.post("https://api.line.me/v2/bot/message/reply", data=json.dumps(req_body), headers=req_header)
    print(r.text)

def get_char_width(c):
    data = unicodedata.east_asian_width(c)
    if data == 'Na' or data == 'H':
        return 1
    return 2

def most_texts(text):
    dic = {}
    for t in text:
        dic[t] = dic.get(t, 0) + 1
    dic = OrderedDict(sorted(dic.items(), key=itemgetter(1), reverse=True))

    for_send_text = ""
    for k,v in dic.items():
        if get_char_width(k) == 1:
            k += " "
        for_send_text += "{0}: {1}\n".format(k, v)
    for_send_text = for_send_text[:-1] # 最後の改行を削除
    return for_send_text

@app.route('/')
def index():
    return u'test'

@app.route('/endpoint', methods=['POST'])
def endpoint():
    reqs = request.json['events']
    for r in reqs:
        if r['type'] == 'message':
            if r['message']['type'] == 'text':
                print(r['replyToken'])
                print(r['message']['text'])
                text = r['message']['text']
                print(text)
                reply_message(r['replyToken'], most_texts(text))
    return jsonify(res='')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
