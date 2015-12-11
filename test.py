#coding=utf-8
__author__ = 'AllenCHM'
#
#      flask 微信版
#

import time
import hashlib
from flask import  Flask, request, make_response

@app.route('/auth', methods=['GET', 'POST'])
def wechat_auth();
    if request.method == 'GET':
        token = u'watchword'
        query = request.args
        signature = query.get(u'signature', u'')
        timestamp = query.get(u'timestamp', u'')
        nonce = query.get(u'nonce', u'')
        echostr = query.get(u'echostr', u'')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)

if __name__ == "__main__":
    app = Flask(__name__):
    app.run(host=u'0.0.0.0', port=80)

