import openai
import json
import os

API_SECRET_KEY = ""
BASE_URL = ""




input_directory = './prompt/logic_prompt' 
output_directory = './result/gpt4o_latest/logic/ori'



def chat_completions3(query):
    client = openai.OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    
    prompt = query+"Please use & | () to represent logic relations. use A B C D respresent basic rules. \nPlease give me the logical relations only with nothing else."
    
    resp = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return resp.choices[0].message.content


def load_queries_from_directory(directory_path):
    queries = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    queries.extend(data) 
    return queries



def load_queries_from_directory(directory_path):
    queries_by_file = {}  
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    queries_by_file[filename] = data  
    return queries_by_file


queries_by_file = load_queries_from_directory(input_directory)


for file_name, queries in queries_by_file.items():
    processed_responses = []

  
    for query in queries:
        response = chat_completions3(query) 
        processed_responses.append(response)

 
    base_name = os.path.splitext(file_name)[0]  
    output_filepath = os.path.join(output_directory, f"{base_name}.json")
    
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(processed_responses, json_file, ensure_ascii=False, indent=4)

    print(f"Processed responses for '{file_name}' have been saved to '{output_filepath}'.")
