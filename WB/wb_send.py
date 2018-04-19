import re
import time 
import json
from logger import logger

url_text_send = "https://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d"
url_pic_send = "http://picupload.service.weibo.com/interface/pic_upload.php?rotate=0&app=miniblog&s=json&mime=image/jpeg&data=1&wm="
Referer = "http://www.weibo.com/u/%s/home?wvr=5"

def upload_image(session, url_pic):
  f = session.get(url_pic, timeout=30)
  img = f.content
  resp = session.post(url_pic_send, data=img)
  upload_json = re.search('{.*}}', resp.text).group(0)
  result = json.loads(upload_json)
  code = result["code"]
  if code == "A00006":
    pid = result["data"]["pics"]["pic_1"]["pid"]
    return pid

def get_wb(pid, text):
  data = {
            "location": "v6_content_home",
            "appkey": "",
            "style_type": "1",
            "pic_id": pid,
            "text": text,
            "pdetail": "",
            "rank": "0",
            "rankid": "",
            "module": "stissue",
            "pub_type": "dialog",
            "_t": "0",
    }
  return data

def send_wb(session,text, url_pic):
  pid = upload_image(session, url_pic)
  data = get_wb(pid, text)
  session.headers["Referer"] = Referer
  session.post(url_text_send % int(time.time() * 1000),data=data)
  t = time.localtime(time.time())
  t = str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)
  logger.info("微博："+text)
  print("微博：",text,t)

