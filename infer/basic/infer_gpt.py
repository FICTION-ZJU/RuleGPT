import openai
import json
import os

API_SECRET_KEY = ""
BASE_URL = ""

# 修改后的 chat_completions3 函数
def chat_completions3(query):
    client = openai.OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    
    prompt = query # + " please give me the answer in the form:\n1.<basic_rule> 2.<basic_rule>..."
    
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return resp.choices[0].message.content

# 从目录读取所有 JSON 文件并提取查询（规则）
def load_queries_from_directory(directory_path):
    queries = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    queries.extend(data)  # 假设每个文件是一个包含字符串的列表
    return queries

# 设置输入和输出目录
input_directory = './prompt/basic_prompt/cn'  # 输入的 JSON 文件夹路径
output_directory = './result/gpt_3.5/basic_rule/ori'  # 输出结果的文件夹路径

# 从输入目录读取查询规则
def load_queries_from_directory(directory_path):
    queries_by_file = {}  # 使用字典来按文件存储查询
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    queries_by_file[filename] = data  # 记录每个文件的查询
    return queries_by_file

# 从输入目录读取查询规则
queries_by_file = load_queries_from_directory(input_directory)

# 逐个文件处理
for file_name, queries in queries_by_file.items():
    processed_responses = []

    # 逐条查询进行处理
    for query in queries:
        response = chat_completions3(query)  # 获取单条查询的处理结果
        processed_responses.append(response)

    # 动态生成输出文件名并保存结果
    base_name = os.path.splitext(file_name)[0]  # 去掉文件扩展名
    output_filepath = os.path.join(output_directory, f"{base_name}.json")
    
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(processed_responses, json_file, ensure_ascii=False, indent=4)

    print(f"Processed responses for '{file_name}' have been saved to '{output_filepath}'.")
