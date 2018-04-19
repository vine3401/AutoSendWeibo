import re
import time
import random
import base64
import binascii
from urllib.parse import quote_plus

import rsa
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)
try:
    input = raw_input
except:
    pass


def getSU(username):
  username_quote = quote_plus(username)
  username_base64 = base64.b64encode(username_quote.encode("utf-8"))
  return username_base64.decode("utf-8")

def get_login_info(su):
  pre_login_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
  pre_login_url = pre_login_url + su +"&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="+str(int(time.time() * 1000)) 
  pre_resp = session.get(pre_login_url, headers=headers)
  login_info = eval(pre_resp.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
  return login_info

def get_cha(pcid):
    cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
    cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
    cha_url = cha_url + pcid
    cha_page = session.get(cha_url, headers=headers)
    with open("cha.jpg", 'wb') as f:
        f.write(cha_page.content)
        f.close()
    try:
        im = Image.open("cha.jpg")
        im.show()
        im.close()
    except:
        print(u"请到当前目录下，找到验证码后输入")


def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd

def login(username, password):
  su = getSU(username)
  login_info = get_login_info(su)
  servertime = login_info["servertime"]
  nonce = login_info["nonce"]
  rsakv = login_info["rsakv"]
  pubkey = login_info["pubkey"]
  showpin = login_info["showpin"]
  password_secret = get_password(password, servertime, nonce, pubkey)
  postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
  login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
  if showpin == 0:
    login_page = session.post(login_url, data=postdata, headers=headers)
  else:
      pcid = login_info["pcid"]
      get_cha(pcid)
      postdata['door'] = input(u"请输入验证码")
      login_page = session.post(login_url, data=postdata, headers=headers)
  login_loop = (login_page.content.decode("GBK"))
  pa = r'location\.replace\([\'"](.*?)[\'"]\)'
  loop_url = re.findall(pa, login_loop)[0]
  login_index = session.get(loop_url, headers=headers)
  uuid = login_index.text
  uuid_pa = r'"uniqueid":"(.*?)"'
  uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
  print(u"登录成功")
  return session, uuid_res