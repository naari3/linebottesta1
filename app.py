#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return u'テスト'

@app.route('/endpoint', methods=['POST'])
def endpoint():
    reqs = request.json['event']
    for r in reqs:
        if r['type'] == 'message':
            if r['message']['type'] == 'text':
                print(r['message']['text'])
    return jsonify(res='ok')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
