#coding=utf-8
__author__ = 'AllenCHM'
#
#      flask 微信版
#

import time
import hashlib
from flask import  Flask, request, make_response
import pymongo
import xml.etree.ElementTree as ET


app = Flask(__name__)

def getContent(fromu):
    conn = pymongo.MongoClient()
    db = conn[u'wJoke']
    doc = db[u'wJoke']
    tmp = doc.find_one_and_update({u'receiver':{u'$nin':[fromu,]}},{u'$addToSet':{u'receiver':fromu}}, {u'content':1})
    return tmp[u'content']


@app.route('/auth', methods=['GET', 'POST'])
def wechat_auth():
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

    if request.method == 'POST':
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        # content = xml_rec.find('Content').text
        content = getContent(fromu)
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())), content))
        response.content_type='application/xml'
        return response


if __name__ == "__main__":

    app.run(host=u'0.0.0.0', port=80)

