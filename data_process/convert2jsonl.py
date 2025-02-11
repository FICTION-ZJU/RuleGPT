import json


input_file = './finetune_data/cn_logic.json'  
output_file = './finetune_data/jsonl/cn_lofic.jsonl' 




with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)


with open(output_file, 'w', encoding='utf-8') as f:
    for entry in data:
        messages = []
        for conv in entry["conversations"]:
            message = {
                "role": conv["from"],
                "content": conv["value"]
            }
            messages.append(message)
        
   
        json.dump({"messages": messages}, f, ensure_ascii=False)
        f.write('\n')  

print("转换完成，输出文件为:", output_file)
