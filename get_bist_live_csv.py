import pandas as pd
from datetime import datetime,timedelta
from selenium import webdriver
import time
import os
from src.upload_s3 import upload_to_s3
import json

def get_bist_live(stock=False):
    output_folder = "daily_bist100"
    os.makedirs(output_folder, exist_ok=True)
    todate = datetime.today().date()
    csv_file_name = f"bist_live_{todate}.csv"
    output_path = os.path.join(output_folder, csv_file_name)

    bist_list = []
    if stock:
        bist_list.append(stock)
        bist100 = bist_list
    else:
        with open("bist100.json","r",encoding="utf-8") as f:
            bist100 = json.load(f)

    current_time = datetime.now().strftime("%H:00")

    df = pd.DataFrame(index=bist100, columns=[current_time])

    try:
        driver = webdriver.Chrome()
        data_dict = {}

        for stock in bist100:
            driver.get(f"https://link-{stock}/")
            driver.implicitly_wait(10)
            driver.execute_script("window.scrollTo(0,10);")
            time.sleep(15)
            stock_name = driver.find_element("xpath","/html/body/div[3]/div[4]/div[2]/div[1]/div[1]/div/div/div/div[2]/button[2]/span[1]/span[1]/div/span[1]").text
            price = driver.find_element("xpath","/html/body/div[3]/div[4]/div[2]/div[1]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/span[1]").text
            data_dict[stock_name] = price

        for stock_name, price in data_dict.items():
            df.loc[stock_name, current_time] = price

        current_date = datetime.now().strftime('%Y-%m-%d')
        output_folder = "daily_bist100"
        os.makedirs(output_folder, exist_ok=True)
        csv_file_name = f"bist_live_{current_date}.csv"
        output_path = os.path.join(output_folder, csv_file_name)

        if os.path.exists(output_path):
            existing_df = pd.read_csv(output_path, index_col=0)
            df = pd.concat([existing_df, df], axis=1)
        df.to_csv(output_path,index_label="stock_name")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()



    #file_path = f"daily_bist100/bist_live_{todate}.csv"
    #folder_name = f"bist_live_daily/"

    #upload_to_s3(file_path, folder_name)


    return df

