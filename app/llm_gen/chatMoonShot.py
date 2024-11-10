import openai
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
# 加载 .env 文件
load_dotenv(verbose=True)
API_BASE = "https://api.moonshot.cn/v1"
API_KEY = os.environ.get("MOONSHOT_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE
)   
def get_MoonShot_response(message,model):
    
    response = client.chat.completions.create(
        model=model,  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": message},
        ],
        # 拓展参数
        extra_body={"temperature": 0.5},
        )
    return response.choices[0].message.content

if __name__ == '__main__':
    print(get_MoonShot_response(model="moonshot-v1-8k",message="你好"))