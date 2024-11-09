import os
import json
import pandas as pd
# 获取当前文件的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 定义主文件夹路径
base_folder = f'{pwd}/../llm_gen/llm_result'
output_excel = f'{pwd}/model_results_axis.xlsx'
real_result_folder = f'{pwd}/../source_handle/handle_data/289538440_按序号_艾森克人格问卷(EPQ-RSC)[复制]_5_5' # 真实结果文件夹名称

# 定义维度题项分配
dimensions = {
    "P": {"positive": [10, 14, 22, 31, 39], "reverse": [2, 6, 18, 26, 28, 35, 43]},
    "E": {"positive": [3, 7, 11, 15, 19, 23, 32, 36, 41, 44, 48], "reverse": [27]},
    "N": {"positive": [1, 5, 9, 13, 17, 21, 25, 30, 34, 38, 42, 46], "reverse": []},
    "L": {"positive": [4, 16, 45], "reverse": [8, 12, 20, 24, 29, 33, 37, 40, 47]}
}

# 反向计分函数
def reverse_score(value):
    return 3 - value  # 假设值在1-2范围内，将2变为1，1变为2

# 计算单个样本的得分
def calculate_scores(data):
    scores = {"P": 0, "E": 0, "N": 0, "L": 0}
    for item in data:
        question_id = item["id"]
        if question_id < 1 or question_id > 48:
            continue
        value = item["value"]
        for dim, items in dimensions.items():
            if question_id in items["positive"]:
                scores[dim] += value
            elif question_id in items["reverse"]:
                scores[dim] += reverse_score(value)
    return scores

# 遍历主文件夹下的各个模型文件夹
excel_writer = pd.ExcelWriter(output_excel, engine='xlsxwriter')
for model_name in os.listdir(base_folder):
    model_path = os.path.join(base_folder, model_name)
    
    # 确保文件夹路径有效且非空
    if os.path.isdir(model_path):
        results = []
        for filename in os.listdir(model_path):
            if filename.endswith('.json'):
                with open(os.path.join(model_path, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    scores = calculate_scores(data)
                    results.append(scores)
        
        # 将每个模型的结果保存到一个 DataFrame 并写入 Excel 的单独工作表
        df = pd.DataFrame(results)
        df.to_excel(excel_writer, sheet_name=model_name, index=False)

# 处理真实结果文件夹
real_result_path = os.path.join(base_folder, real_result_folder)
if os.path.isdir(real_result_path):
    real_results = []
    for filename in os.listdir(real_result_path):
        if filename.endswith('.json'):
            with open(os.path.join(real_result_path, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                scores = calculate_scores(data)
                real_results.append(scores)
    
    # 将真实结果保存为一个单独的工作表
    real_df = pd.DataFrame(real_results)
    real_df.to_excel(excel_writer, sheet_name='Real Result', index=False)

# 保存并关闭 Excel 文件
excel_writer._save()
