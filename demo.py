import base64
import binascii
import re
import json

import rsa
import requests

USER_AGENT = (
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
      'Chrome/20.0.1132.57 Safari/536.11'
)

def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)

def wblogin(username="18482065251",password="Lz122521#"):
  session = requests.session()
  session.headers['User-Agent'] = USER_AGENT
  su = base64.b64encode(username.encode("utf-8"))
  resp = session.get("https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)" % su)
  pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
  pre_login = json.loads(pre_login_str)
  data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(requests.utils.quote(username).encode('utf-8')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': encrypt_passwd(password, pre_login['pubkey'],pre_login['servertime'], pre_login['nonce']),
        'rsakv': pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '53',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
  login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
  resp = session.post(login_url, data=data)
  match_obj = re.search('replace\(\"([^\']+)\"\)', resp.text)
  if match_obj is None:
    print("失败")
  login_url = match_obj.group(1)
  resp = session.get(login_url)
  login_str = re.search('replace\(\'([^\']+)\'\)', resp.text).group(1)
  resp = session.get(login_str)
  content = re.search('\((\{.*\})\)', resp.text).group(1)
  user = json.loads(content)
  uid = user.get("userinfo").get("uniqueid")
  data = {
      "location": "v6_content_home",
      "appkey": "",
      "style_type": "1",
      "pic_id": "",
      "text": "Something interesting",
      "pdetail": "",
      "rank": "0",
      "rankid": "",
      "module": "stissue",
      "pub_type": "dialog",
      "_t": "0",
  }
wblogin()