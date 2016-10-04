#!/bin/env python
# coding: utf-8

import os
import json
from flask import Flask, render_template, request, jsonify
import requests

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

@app.route('/')
def index():
    return u'テスト'

@app.route('/endpoint', methods=['POST'])
def endpoint():
    reqs = request.json['events']
    for r in reqs:
        if r['type'] == 'message':
            if r['message']['type'] == 'text':
                print(r['replyToken'])
                print(r['message']['text'])
                reply_message(r['replyToken'], r['message']['text'])
    return jsonify(res='ok')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
