import json
from datetime import datetime,timedelta
from selenium import webdriver
import time
import os
from src.upload_s3 import upload_to_s3

def get_bist_live(stock=False):
    # Define output folder
    output_folder = "daily_bist100"
    # Create folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    todate = datetime.today().date()
    json_file_name = f"bist_live_{todate}.json"
    output_path = os.path.join(output_folder, json_file_name)

    bist_list = []
    if stock:
        bist_list.append(stock)
        bist100 = bist_list
    else:
        with open("bist100.json","r",encoding="utf-8") as f:
            bist100 = json.load(f)

    try:
        driver = webdriver.Chrome()
        data_list = []

        # Önce var olan verileri oku
        if os.path.exists(output_path):
            with open(output_path, 'r') as json_file:
                data_list = json.load(json_file)

        for stock in bist100:
            driver.get(f"https://link-{stock}/")
            driver.implicitly_wait(10)
            driver.execute_script("window.scrollTo(0,10);")
            time.sleep(15)
            stock_name = driver.find_element("xpath", "/html/body/div[3]/div[4]/div[2]/div[1]/div[1]/div/div/div/div[2]/button[2]/span[1]/span[1]/div/span[1]").text
            price = driver.find_element("xpath", "/html/body/div[3]/div[4]/div[2]/div[1]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/span[1]").text

            current_time = datetime.now().strftime("%Y-%m-%d %H:%00")
            data_list.append({stock_name: {'time': current_time, 'price': price}})
            
        with open(output_path, 'w') as json_file:
            json.dump(data_list, json_file, indent=4)
            print(f"JSON file created for today's data: {output_path}")

        # Print the JSON output
        print(json.dumps(data_list, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    file_path = f"daily_bist100/bist_live_{todate}.json"
    folder_name = f"bist_live_daily/"

    upload_to_s3(file_path, folder_name)


    return data_list
