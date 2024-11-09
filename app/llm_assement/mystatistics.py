import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from data_prepare import true_results, model_predictions,sample_ids
# 假设您已经有以下变量：
# sample_ids: 样本 ID 的列表
# true_results: 真实结果列表，每个元素是一个样本的回答列表
# model_predictions: 模型预测结果的字典，键为模型名称，值为预测结果列表


# 示例：
# sample_ids = ['sample1', 'sample2', 'sample3', ...]
# true_results = [[1, 2, 1, ..., 2], [2, 1, 1, ..., 1], [1, 1, 2, ..., 2], ...]
# model_predictions = {
#     'gpt-3.5-turbo': [[1, 2, 1, ..., 2], [2, 2, 1, ..., 1], [1, 1, 1, ..., 2], ...],
#     'gpt-4': [...],
#     'chatGLM': [...],
#     # 其他模型
# }
# 初始化一个 DataFrame，用于存储结果
df_results = pd.DataFrame({'Sample ID': sample_ids})

# 将 true_results 转换为字典，方便后续查找
true_results_dict = dict(zip(sample_ids, true_results))

# 遍历每个模型，计算每个样本的准确率
for model_name, predictions in model_predictions.items():
    accuracies = []
    for sample_id, y_pred in zip(sample_ids, predictions):
        y_true = true_results_dict[sample_id]
        # 计算该样本在该模型下的准确率
        acc = accuracy_score(y_true, y_pred)
        accuracies.append(acc)
    # 将结果添加到 DataFrame
    df_results[model_name] = accuracies
# 设置 'Sample ID' 为索引
df_results.set_index('Sample ID', inplace=True)

# 打印结果
print(df_results)

from statsmodels.stats.contingency_tables import mcnemar
def mcnemar_test(y_true_list, y_pred_list1, y_pred_list2):
    """
    对于同一组真实标签，比较两个预测结果之间的差异
    """
    # 将所有样本的预测结果和真实结果展开为一维数组
    y_true = np.concatenate(y_true_list)
    y_pred1 = np.concatenate(y_pred_list1)
    y_pred2 = np.concatenate(y_pred_list2)
    
    # 计算模型1和模型2的预测是否与真实结果一致
    correct1 = (y_pred1 == y_true)
    correct2 = (y_pred2 == y_true)
    
    # 构建 2x2 计数表
    # b: 模型1预测错误，模型2预测正确的样本数
    # c: 模型1预测正确，模型2预测错误的样本数
    b = np.sum(~correct1 & correct2)
    c = np.sum(correct1 & ~correct2)
    
    table = [[0, b],
             [c, 0]]
    
    # 执行 McNemar 检验
    result = mcnemar(table, exact=True)
    return result.pvalue
# 定义一个字典，存储每个模型的 p 值
model_pvalues = {}

for model_name, predictions in model_predictions.items():
    # 计算 McNemar 检验的 p 值
    pvalue = mcnemar_test(true_results, predictions, true_results)
    model_pvalues[model_name] = pvalue

# 输出结果
for model_name, pvalue in model_pvalues.items():
    print(f"模型 {model_name} 与真实结果的 McNemar 检验 p 值：{pvalue:.4f}")
    if pvalue < 0.05:
        print("结果具有统计显著性差异。")
    else:
        print("结果没有统计显著性差异。")
    print("-" * 30)
from itertools import combinations

model_names = list(model_predictions.keys())
model_pairs = list(combinations(model_names, 2))

for model1, model2 in model_pairs:
    predictions1 = model_predictions[model1]
    predictions2 = model_predictions[model2]
    pvalue = mcnemar_test(true_results, predictions1, predictions2)
    print(f"模型 {model1} 与模型 {model2} 的 McNemar 检验 p 值：{pvalue:.4f}")
    if pvalue < 0.05:
        print("两模型之间预测结果具有统计显著性差异。")
    else:
        print("两模型之间预测结果没有统计显著性差异。")
    print("-" * 30)

import seaborn as sns
import matplotlib.pyplot as plt
# 设置字体为 SimHei 以支持中文显示（也可以尝试 'Microsoft YaHei'）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 重置索引以便绘图
df_results_reset = df_results.reset_index()
# 将数据转换为长格式，便于绘图
df_results_melt = df_results_reset.melt(id_vars="Sample ID", var_name="Model", value_name="Accuracy")

# 使用转换后的数据绘制热力图
heatmap_data = df_results_melt.pivot(index="Sample ID", columns="Model", values="Accuracy")
plt.figure(figsize=(20, len(sample_ids) // 1.5))  # 增高热力图
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt=".2f")
plt.title('模型在各样本上的正确率热力图')
plt.xlabel('模型')
plt.ylabel('样本 ID')
plt.show()

# 计算每个模型的平均正确率
average_accuracies = df_results.mean()

# 绘制柱状图
plt.figure(figsize=(10, 8))
bars = average_accuracies.plot(kind='bar')
plt.ylabel('平均正确率')
plt.title('各模型平均正确率比较')
plt.ylim(0.5, 0.7)  # 缩小纵轴范围
plt.xticks(rotation=45)

# 为每个柱添加准确率标签
for bar in bars.containers[0]:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height - 0.02, f'{height:.2%}', ha='center', va='bottom', fontsize=10)

plt.show()
