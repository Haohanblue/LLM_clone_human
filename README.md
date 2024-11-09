# LLM_clone_human
Python版本 3.11.9
# 下载poetry管理环境
```
pip install poetry 
```
# 创建poetry虚拟环境
```
poetry shell
```
# 下载依赖
```
poetry install
```
在项目根目录创建一个.env文件。
里面放入 
OPENAI_API_KEY="你的openai Key"
ZHIPUAI_API_KEY="你的zhipuai Key"

# 项目目录结构

|-- app
    |-- history   *存放历史记录*
    |-- llm_assement  *llm评估模块*
    |   |-- assement.py *结果输出与评估*
    |   |-- data_prepare.py *数据准备*
    |   |-- heat.py *输出全样本相似度矩阵*
    |   |-- mystatistics.py *基本统计*
    |   |-- other.py *和其他样本相比*
    |   |-- result.py *特例计算*
    |   |-- weight.py *生成维度计算*
    |-- llm_gen    *llm预测模块*
    |   |-- chatGLM.py  *GLM的模块*
    |   |-- chatGPT.py *GPT的模块*
    |   |-- genarate.py *开始预测*
    |   |-- process_log.log *输出日志*
    |   |-- progress.json *进度控制*
    |   |-- template.py *提示词模版*
    |   |-- llm_result *存放各个模型预测的结果文件*
    |   |   |-- chatgpt-4o-latest *模型名称* 
    |   |   |   |-- llm_result_13271097380.json *预测结果*
    |   |   |-- GLM-4-Flash
    |   |   |-- gpt-3.5-turbo
    |   |   |-- gpt-4-turbo
    |   |   |-- gpt-4o-mini
    |   |
    |-- source_handle *源文件处理模块*
        |-- gen_blank_question.py *生成空白问卷*
        |-- get_result.py *获得结果*
        |-- handle_source.py *处理源文件*
        |-- handle_data *数据存放*
        |   |-- 289538440_按序号_艾森克人格问卷(EPQ-RSC)[复制]_5_5 *测试集量表*
        |   |   |-- result_13271097380.json *标签数据*
        |   |-- 289539715_按序号_【24-FAL】(DAY1) 中国大五人格问卷简版（CBF-PI-B）[复制]_5_5 *训练集量表*
        |   |   |-- result_13271097380.json *训练样本数据*
        |-- source_data *存放问卷星导出的excel*
            |-- 289538440_按序号_艾森克人格问卷(EPQ-RSC)[复制]_5_5.xlsx
            |-- 289539715_按序号_【24-FAL】(DAY1) 中国大五人格问卷简版（CBF-PI-B）[复制]_5_5.xlsx
