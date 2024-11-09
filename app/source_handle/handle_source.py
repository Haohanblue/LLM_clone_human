import pandas as pd
import json
import os
import math

# 获取当前文件所在的目录
pwd = os.path.dirname(os.path.abspath(__file__))

# 设置输入和输出目录
source_data_dir = f'{pwd}/source_data'
output_base_dir = f'{pwd}/handle_data'

# 遍历source_data目录中的所有xlsx文件
for file_name in os.listdir(source_data_dir):
    if file_name.endswith('.xlsx'):
        excel_file_path = os.path.join(source_data_dir, file_name)
        output_dir = os.path.join(output_base_dir, os.path.splitext(file_name)[0])
        
        # 创建输出目录，如果不存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取Excel文件
        df = pd.read_excel(excel_file_path)
        
        # 遍历每一行，将每行保存为单独的JSON文件
        sample_id = 1  # 样本ID
        for _, row in df.iterrows():
            json_list = []
            question_id = 1  # 题号ID，每次从1开始
            
            phone_number = None  # 初始化手机号变量
            
            for col in df.columns:
                value = row[col]
                
                # 检查是否为 '联系方式（手机号）' 或 '联系方式'，获取手机号
                if col == '联系方式（手机号）' or col == '联系方式':
                    phone_number = str(value).strip()  # 将手机号转换为字符串并去除空格
                
                # 尝试将 value 转换为整数，如果失败则保留原值
                try:
                    int_value = int(value)
                except (ValueError, TypeError):
                    int_value = value  # 保留原始值，可能是字符串或其他类型
                
                # 创建一个选项的key-value对象
                json_object = {
                    "id": question_id,
                    "description": col,
                    "value": int_value
                }
                json_list.append(json_object)
                question_id += 1
            
            # 如果没有找到手机号，使用样本ID作为文件名
            if phone_number is None:
                file_name_json = f'result_{sample_id}.json'
            else:
                file_name_json = f'result_{phone_number}.json'
            
            # 将列表写入JSON文件
            json_file_path = os.path.join(output_dir, file_name_json)
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_list, json_file, ensure_ascii=False, indent=4)
            
            sample_id += 1  # 更新样本ID
        
        print(f"{file_name} 中的问卷结果已保存到 {output_dir}。")
