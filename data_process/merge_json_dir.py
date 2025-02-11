import json
import os


input_dir = './finetune_data'  
output_file = 'llama3_verycreative_prompt_200k_thres025_answer_t1_1.json'

merged_data = []


for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    
    
    if filename.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  
            if isinstance(data, list):  
                merged_data.extend(data) 

with open(output_file, 'w', encoding='utf-8') as output:
    json.dump(merged_data, output, ensure_ascii=False, indent=4)

print(f"All files have been merged into {output_file}")
