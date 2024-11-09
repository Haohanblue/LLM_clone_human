import json
import os
#获取当前文件所在的目录
pwd = os.path.dirname(os.path.abspath(__file__))


def calculate_similarity(llm_file, source_file):
    # 读取 JSON 文件
    with open(llm_file, 'r', encoding='utf-8') as f:
        llm_data = json.load(f)
        
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
        
    # 提取id为1到48的value值并进行比较
    matching_count = 0
    total_count = 0
    
    for llm_item, source_item in zip(llm_data, source_data):
        # 只比较id为1到48的条目
        if 1 <= llm_item["id"] <= 48:
            total_count += 1
            if llm_item["value"] == source_item["value"]:
                matching_count += 1
    # 计算相似度（正确率）
    similarity = (matching_count / total_count) * 100 if total_count > 0 else 0
    return f"{similarity:.2f}%"

# 使用文件路径调用函数
print("LLM和方俊杰的相似度为",calculate_similarity(f"{pwd}/llm_result_1.json", f"{pwd}/source_result_1.json"))
print("LLM和第二个人的相似度为",calculate_similarity(f"{pwd}/llm_result_1.json", f"{pwd}/result_2.json"))
print("LLM和第三个人的相似度为",calculate_similarity(f"{pwd}/llm_result_1.json", f"{pwd}/result_3.json"))
print("方俊杰和第二个人的相似度为",calculate_similarity(f"{pwd}/result_2.json", f"{pwd}/source_result_1.json"))
print("方俊杰和第三个人的相似度为",calculate_similarity(f"{pwd}/result_3.json", f"{pwd}/source_result_1.json"))

