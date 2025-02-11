from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import os
import torch

device = "cuda:0"  # the device to load the model onto
# os.environ["CUDA_VISIBLE_DEVICES"] = "4,5,6,7"
model_name_or_path = "./all_models/Qwen2.5-7B-Instruct_1111"

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)


def load_json_files_from_directory(directory_path):
    json_data = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_data[filename] = data  
    return json_data



def process_rules(rules):
    processed_results = []
    patterns = [
    'object action object',
    'object action',
    'action object',
    'object attribute compare value',
    'action attribute compare value',
    'object adjective'
]
    
    for rule in rules:
        need_regeneration = True
        num = 0
        output_str = ""
        last_output_str = ""
        prompt = rule  + "Please give me the answer only with nothing else."

        while need_regeneration:
            # Reset flag and output string
            need_regeneration = False
            
            # Prepare model inputs
            messages = [
                {"role": "user", "content": prompt}
            ]
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = tokenizer([text], return_tensors="pt").to(device)

            # Generate the output
            generated_ids = model.generate(
                model_inputs.input_ids,
                max_new_tokens=512
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            output_str += response
            num += 1
            last_output_str = output_str
            print(last_output_str)

            
            output_matched = any(pattern in output_str for pattern in patterns)

            
            if output_matched:
                processed_results.append(output_str)
                need_regeneration = False
            if num >100:
                need_regeneration = False
        if not output_matched:
            processed_results.append(last_output_str)
        
    return processed_results


input_directory = './prompt/grammar_prompt' 
output_directory = './result/2.5_7b_ori/grammar'  

json_files = load_json_files_from_directory(input_directory)


for filename, rules in json_files.items():
    if isinstance(rules, list):  
        processed_results = process_rules(rules)
        
     
        base_name = os.path.splitext(filename)[0]  
        output_filepath = os.path.join(output_directory, f"{base_name}.json")
        
        
        with open(output_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(processed_results, json_file, ensure_ascii=False, indent=4)

        print(f"Processed results for '{filename}' have been saved to '{output_filepath}'.")

