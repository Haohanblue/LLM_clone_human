import os
import json
pwd = os.path.dirname(os.path.abspath(__file__))
# 定义文件夹路径
llm_result_dir = f'{pwd}/llm_result'

# 检查每个模型文件夹
for model_name in os.listdir(llm_result_dir):
    model_dir = os.path.join(llm_result_dir, model_name)
    if not os.path.isdir(model_dir):
        continue

    # 检查每个样本文件
    for sample_file in os.listdir(model_dir):
        sample_path = os.path.join(model_dir, sample_file)
        if not sample_file.endswith('.json'):
            continue

        try:
            with open(sample_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 检查 id 是否从 1 到 48 且 value 只能为 1 或 2
            ids = set()
            invalid_value = False
            for entry in data:
                if entry['value'] not in [1, 2]:
                    invalid_value = True
                ids.add(entry['id'])

            # 判断 id 是否完整和 value 是否有效
            missing_ids = set(range(1, 49)) - ids
            if missing_ids or invalid_value:
                print(f"模型: {model_name}, 样本文件: {sample_file}")
                if missing_ids:
                    print(f"缺少的 id: {sorted(missing_ids)}")
                if invalid_value:
                    print("存在不符合要求的 value 值（非1或2）")

        except json.JSONDecodeError:
            print(f"模型: {model_name}, 样本文件: {sample_file} 的 JSON 格式有误")
        except Exception as e:
            print(f"模型: {model_name}, 样本文件: {sample_file} 检查过程中出错: {e}")

print("检查完成。")
