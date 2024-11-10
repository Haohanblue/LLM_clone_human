from zhipuai import ZhipuAI
from dotenv import load_dotenv
load_dotenv(verbose=True)
import os 
# 获取单个环境变量的值
api_key = os.environ.get('ZHIPUAI_API_KEY')
client = ZhipuAI(api_key=api_key)  # 填写您自己的APIKey

def get_zhipu_respnse(message,model):
    
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
    print(get_zhipu_respnse(model="charglm-3",message="你好"))