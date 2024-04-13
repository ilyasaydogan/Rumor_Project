import google.generativeai as genai
import json
from datetime import datetime,timedelta
import os
import yaml
from src.upload_s3 import upload_to_s3

def get_analysis_output():
    with open("/Users/dursun/Desktop/Rumor_Project/config.yml", "r") as file:
        config = yaml.safe_load(file)

    start_time = datetime.now()
    todate = datetime.today().date()

    with open(f'statement_output/{todate}/statement_{todate}.json') as f :
        data = json.load(f)

    comment_list=[]
    for i in data:
        comment = {}
        prompt = f"Bu KAP bildirimini oku, profesyonel finansal okuryazarlığı olmayan biri için olumlu ya da olumsuz veya hem olumlu hem de olumsuz bir şekilde değerlendir + {i['text']}"
        genai.configure(api_key="****")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        prompt_parts = [prompt]

        response = model.generate_content(prompt_parts)
        comment['disc_index'] = i['disc_index']
        comment['ticker'] =i['company_name']
        comment['comment'] = response.text
        comment['date'] = todate
        comment_list.append(comment)

    output_folder = "analysis_results"  
    folder_path = os.path.join(output_folder, str(todate))
    os.makedirs(folder_path, exist_ok=True) 
    folder_path = os.path.join(output_folder, str(todate))
    json_file_name = f"analysis_results_{todate}.json"
    output_path = os.path.join(folder_path, json_file_name)

    for i in comment_list:
        i['date']=str(i['date'])
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comment_list, f, ensure_ascii=False, indent=4)

    end_time = datetime.now()
    duration = end_time-start_time

    file_path = f"analysis_results/{todate}/analysis_results_{todate}.json"
    folder_name = f"KAP/KAP_analysis/"

    upload_to_s3(file_path, folder_name)
    print(f"Duration : {duration} min")
    
    return comment_list
    

