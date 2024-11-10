# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import os
load_dotenv(verbose=True)
import requests
import time
import hashlib
import json

url = 'https://api-maas.singularity-ai.com/sky-work/api/v1/chat'
app_key = os.environ.get("SKY_API_KEY")       # 这里需要替换你的APIKey
app_secret = os.environ.get("SKY_SECRET_KEY")  # 这里需要替换你的APISecret
timestamp = str(int(time.time()))
sign_content = app_key + app_secret + timestamp
sign_result = hashlib.md5(sign_content.encode('utf-8')).hexdigest()


# 设置请求头，请求的数据格式为json
headers={
   "app_key": app_key,
   "timestamp": timestamp,
   "sign": sign_result,
   "Content-Type": "application/json",
}
def get_sky_response(message,model):
    data = {
        "messages": [
            {"role": "user", "content": message}
        ],
        "intent": "" # 用于强制指定意图，默认为空将进行意图识别判定是否搜索增强，取值 'chat'则不走搜索增强
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    for line in response.iter_lines():
        if line:
            return json.loads(line.decode('utf-8'))[0]['content']


if __name__ == '__main__':
    print(get_sky_response(model="sky-1",message="你好"))