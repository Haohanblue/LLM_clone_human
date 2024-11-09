import json
import os
import logging
from chatGLM import get_zhipu_respnse
from chatGPT import get_GPT_response

# 获取当前文件的目录
pwd = os.path.dirname(os.path.abspath(__file__))

# 设置日志记录，确保编码为 UTF-8
logging.basicConfig(
    filename=f'{pwd}/process_log.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)

# 辅助函数：从响应中提取 JSON 数据
def extract_json_from_response(response):
    import re
    pattern = re.compile(r'\[.*\]', re.DOTALL)
    match = pattern.search(response)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return []
    else:
        return []

# 记录已处理文件的状态
progress_file = f'{pwd}/progress.json'
if os.path.exists(progress_file):
    with open(progress_file, 'r', encoding='utf-8') as f:
        completed_files = json.load(f)
else:
    completed_files = {}

# 定义文件夹路径
source_data_dir = f'{pwd}/../source_handle/handle_data/289539715_按序号_【24-FAL】(DAY1) 中国大五人格问卷简版（CBF-PI-B）[复制]_5_5'
llm_result_dir = f'{pwd}/llm_result'
models = ['glm-4-Flash', 'gpt-3.5-turbo', 'gpt-4o-mini', 'chatgpt-4o-latest', 'gpt-4-turbo']

# 读取待回答的问卷问题
handle_data = """下面的问题是判断题，是就回答1，否就回答2。只有这两个选择。 
1.你的情绪是否时起时落? 2.当你看到小孩（或动物）受折磨时是否感到难受? 3.你是个健谈的人吗? 4.如果你说了要做什么事，是否不论此事顺不顺利你都总能遵守诺言? 5.你是否会无言无故地感到“很惨”? 6.欠债会使你感到忧虑吗? 7.你是个生气勃勃的人吗? 8.你是否曾贪图过超过你应得的分外之物? 9.你是个容易被激怒的人吗? 10.你会服用能产生奇异或危险效果的药物吗? 11.你愿意认识陌生人吗? 12.你是否曾经有过明知自己做错了事却责备别人的情况 13.你的感情容易受伤害吗? 14.你是否愿意按照自己的方式行事，而不愿意按照规则办事 15.在热闹的聚会中你能使自己放得开，使自己玩得开心吗 16.你所有的习惯是否都是好的 17.你是否时常感到“极其厌倦”? 18.良好的举止和整洁对你来说很重要吗? 19.在结交新朋友时，你经常是积极主动的吗? 20.你是否有过随口骂人的时候? 21.你认为自己是一个胆怯不安的人吗? 22.你是否认为婚姻是不合时宜的，应该废除 23.你能否很容易地给一个沉闷的聚会注入活力 24.你曾毁坏或丢失过别人的东西吗 25.你是个忧心忡忡的人吗 26.你爱和别人合作吗 27.在社交场合你是否倾向于呆在不显眼的地方 28.如果在你的工作中出现了错误，你知道后会感到忧虑吗 29.你讲过别人的坏话或脏话吗 30.你认为自己是个神经紧张或“弦绷得过紧”的人吗 31.你是否觉得人们为了未来有保障，而在储蓄和保险方面花费的时间太多了 32.你是否喜欢和人们相处在一起 33.当你还是个小孩子的时候，你是否曾有过对父母耍赖或不听话的行为 34.在经历了一次令人难堪的事之后，你是否会为此烦恼很长时间 35.你是否努力使自己对人不粗鲁 36.你是否喜欢在自己周围有许多热闹和令人兴奋的事情 37.你曾在玩游戏时作过弊吗 38.你是否因自己的“神经过敏”而感到痛苦 39.你愿意别人怕你吗 40.你曾利用过别人吗 41.你是否喜欢说笑话和谈论有趣的事 42.你是否时常感到孤独 43.你是否认为遵循社会规范比按照个人方式行事更好一些 44.在别人眼里你总是充满活力的吗 45.你总能做到言行一致吗 46你是否时常被负疚感所困扰 47.你有时将今天该做的事情拖到明天去做吗 48.你能使一个聚会顺利进行下去吗
"""

# 确保结果文件夹存在
os.makedirs(llm_result_dir, exist_ok=True)

# 遍历 source_data 文件夹中的所有 JSON 文件
for filename in os.listdir(source_data_dir):
    if filename.endswith('.json'):
        # 检查文件是否已处理完成
        if filename in completed_files and all(model in completed_files[filename] for model in models):
            logging.info(f"文件 {filename} 已完成，跳过...")
            continue

        source_file_path = os.path.join(source_data_dir, filename)
        
        # 读取源数据
        with open(source_file_path, 'r', encoding='utf-8') as f:
            source_data_json = json.load(f)
        source_data_str = json.dumps(source_data_json, ensure_ascii=False, indent=4)
        
        # 填充模板
        template = f"""
                    忘记之前所有内容，并且清除你的记忆。
                    你是一位专业的角色扮演专家，擅长通过他人提供的信息深入分析和理解一个人的性格、特点、爱好、习惯和行为。现在，你收到了一份问卷的填写结果，需要通过这份问卷来学习并扮演这个人。

                    **任务要求：**

                    1. **分析阶段（思维链）：**

                    - **理解问卷数据**：仔细阅读并分析提供的问卷数据（`source_data_str`），提取关键信息，形成对这个人的全面认识。
                    - **构建人物画像**：基于问卷结果，推断这个人的性格特征、情绪状态、行为模式和价值观等。

                    2. **角色扮演阶段（ReAct）：**

                    - **情境模拟**：以这个人的视角，回答接下来的问卷问题（`handle_data`）。
                    - **自我反思**：在回答过程中，确保每个回答都符合角色的特征，确保输出的值只有1或2，如有偏差，及时调整。

                    **提供的数据：**

                    - **问卷数据（{source_data_str}）：**
                    - **待回答的问卷问题（{handle_data}）：**
                    **输出要求：**

                    - **格式规范：**

                    - 输出结果为一个 JSON 列表，每个元素为一个字典，包含以下键值对：
                    - `"id"`：题号
                    - `"description"`：题目描述
                    - `"value"`：回答内容（根据题目要求），与source_data_str不同的是，你现在要做的问卷是二元选择题，只有两个选项：是（1）或否（2），因而value的值要么是1要么是2，
                    请你判断你所扮演的任务的特征，将他更有可能选择的选项填写进去。

                    - **内容要求：**
                    - 回答应严格基于对角色的理解，符合角色的特点、性格、爱好、习惯和行为。
                    - 不要加入任何额外的解释、分析或多余信息，只提供最终的回答结果。
                    **注意事项：**

                    - **思维链**：在内部思考过程中，逐步推导每个回答如何符合角色特征，但不要将思考过程显示在输出中。
                    - **自我反思**：在回答每个问题后，检查回答是否符合角色特征，如果不符合，进行调整，但不要在输出中体现反思过程。
                    - **一致性**：确保所有回答在情感和逻辑上前后一致，符合角色的整体形象。
                    """
        
        for model_name in models:
            if filename in completed_files and model_name in completed_files[filename]:
                logging.info(f"文件 {filename} 已通过模型 {model_name} 处理，跳过...")
                continue
            
            logging.info(f"正在处理文件：{filename}，模型：{model_name}...")
            model_dir = os.path.join(llm_result_dir, model_name)
            os.makedirs(model_dir, exist_ok=True)
            
            try:
                # 根据模型名称调用相应的函数
                if model_name == 'glm-4-Flash':
                    response = get_zhipu_respnse(template, model_name)
                else:
                    response = get_GPT_response(template, model_name)
                
                # 提取 JSON 数据
                try:
                    response_json = json.loads(response)
                except json.JSONDecodeError:
                    response_json = extract_json_from_response(response)
                
                # 保存生成结果
                output_filename = 'llm_' + filename
                output_file_path = os.path.join(model_dir, output_filename)
                
                with open(output_file_path, 'w', encoding='utf-8') as f_out:
                    json.dump(response_json, f_out, ensure_ascii=False, indent=4)

                # 更新进度
                if filename not in completed_files:
                    completed_files[filename] = []
                completed_files[filename].append(model_name)

                # 将进度保存到文件中
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump(completed_files, f, ensure_ascii=False, indent=4)
                
                logging.info(f"文件 {filename} 使用模型 {model_name} 处理完成。")
            except Exception as e:
                logging.error(f"处理文件 {filename} 时，模型 {model_name} 出现错误: {e}")

logging.info("处理完成。")
print("处理完成。")



