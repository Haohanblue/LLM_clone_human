import numpy as np
from sklearn.metrics import accuracy_score
from scipy.stats import ttest_ind, wilcoxon
import pandas as pd
from data_prepare import true_results, model_predictions,sample_ids

def perform_statistical_tests(sample_ids, true_results, model_predictions):
    """
    对每个样本和每个模型进行检验，比较模型预测结果与目标样本和其他样本的相似性。
    返回一个包含检验结果的 DataFrame。
    """
    results = []  # 用于存储每个检验结果的列表

    num_samples = len(sample_ids)
    sample_id_to_index = {sample_id: idx for idx, sample_id in enumerate(sample_ids)}

    for model_name, predictions in model_predictions.items():
        print(f"正在处理模型：{model_name}")
        for target_idx, sample_id in enumerate(sample_ids):
            y_true_target = true_results[target_idx]
            y_pred_target = predictions[target_idx]

            # 计算模型预测与目标样本真实结果的相似性
            similarity_with_target = accuracy_score(y_true_target, y_pred_target)

            # 计算模型预测与其他样本真实结果的相似性
            similarities_with_others = []
            for other_idx in range(num_samples):
                if other_idx != target_idx:
                    y_true_other = true_results[other_idx]
                    # 使用目标样本的模型预测结果 y_pred_target
                    similarity_with_other = accuracy_score(y_true_other, y_pred_target)
                    similarities_with_others.append(similarity_with_other)
            # 将相似性列表转换为 numpy 数组
            similarities_with_others = np.array(similarities_with_others)

            # 统计检验：判断模型与目标样本的相似性是否显著高于与其他样本的相似性
            # 检查数据分布，选择适当的检验方法
            # 由于数据可能不满足正态性，使用非参数检验 Wilcoxon 符号秩检验
            # 但是 Wilcoxon 符号秩检验要求两组数据长度相同，这里可以使用 Mann-Whitney U 检验

            from scipy.stats import mannwhitneyu

            U_statistic, p_value = mannwhitneyu(
                [similarity_with_target], similarities_with_others, alternative='greater'
            )

            # 判断是否具有统计显著性差异
            significance = p_value < 0.05

            # 记录结果
            result = {
                'Sample ID': sample_id,
                'Model': model_name,
                'Similarity with Target': similarity_with_target,
                'Mean Similarity with Others': np.mean(similarities_with_others),
                'U Statistic': U_statistic,
                'p-value': p_value,
                'Significant': significance
            }
            results.append(result)

    # 将结果转换为 DataFrame
    df_results = pd.DataFrame(results)
    return df_results
# 调用函数
df_test_results = perform_statistical_tests(sample_ids, true_results, model_predictions)

# 查看结果
print(df_test_results)