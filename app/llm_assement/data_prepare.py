import os
import json
# 获取当前文件夹下的路径
pwd = os.path.dirname(os.path.abspath(__file__))

def load_data(data_dir):
    """
    从包含 JSON 文件的目录加载数据。
    每个 JSON 文件包含一个字典列表，每个字典有 'id'、'description' 和 'value'。
    返回一个字典，键为样本 ID，值为按 'id' 从 1 到 48 排序的 'value' 列表。
    """
    data = {}
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
                # 按 'id' 对数据进行排序
                sample_data_sorted = sorted(sample_data, key=lambda x: int(x['id']))
                # 提取 'id' 在 1 到 48 之间的 'value' 值
                values = [item['value'] for item in sample_data_sorted if 1 <= int(item['id']) <= 48]
                # 提取数字部分作为样本 ID（去掉前缀）
                sample_id = ''.join(filter(str.isdigit, os.path.splitext(filename)[0]))
                data[sample_id] = values
    return data

def load_model_predictions(models_dir):
    """
    从包含模型预测结果的目录加载数据。
    假设 models_dir 包含以模型名称命名的子目录，每个子目录包含模型的预测结果 JSON 文件。
    返回一个字典，键为模型名称，值为一个字典，包含样本 ID 和对应的预测值列表。
    """
    model_predictions = {}
    for model_name in os.listdir(models_dir):
        model_dir = os.path.join(models_dir, model_name)
        if os.path.isdir(model_dir):
            model_data = load_data(model_dir)
            model_predictions[model_name] = model_data
    return model_predictions

# 设置真实结果和模型预测结果目录路径
true_results_dir = f'{pwd}/../source_handle/handle_data/289538440_按序号_艾森克人格问卷(EPQ-RSC)[复制]_5_5'  # 真实结果目录路径
models_dir = f'{pwd}/../llm_gen/llm_result'  # 模型预测结果目录路径

# 加载真实结果和模型预测结果
true_data = load_data(true_results_dir)
model_predictions_data = load_model_predictions(models_dir)

# 获取对齐的样本 ID
sample_ids = set(true_data.keys())
for model_name, predictions in model_predictions_data.items():
    sample_ids = sample_ids & set(predictions.keys())

sample_ids = sorted(sample_ids)

# 构建 true_results 和 model_predictions
true_results = [true_data[sample_id] for sample_id in sample_ids]
model_predictions = {
    model_name: [predictions[sample_id] for sample_id in sample_ids]
    for model_name, predictions in model_predictions_data.items()
}
