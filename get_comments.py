#########  Importing Library  #########

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import random
import pandas as pd
from datetime import datetime
import re
import json
import os
import json
from src.upload_s3 import upload_to_s3

def get_comments ():

    #########  Getting Links and Stocks #########

    trade_links_dict = {} # Creating dictionary to store the trade and links information

    # Assuming 'table_lines' contains the lines of your table
    # You can read the table from a file or any other source
    table_lines1 = ["AEFES\tlink1\tlink2\tlink3\tlink4\tlink5","AGHOL\tlink1\tlink2\tlink3\tlink4\tlink5"]

    table_lines2 = ["MAVI\tlink1\tlink2\tlink3\tlink4\tlink5","PENTA\tlink1\tlink2\tlink3\tlink4\tlink5"]

    table_lines = table_lines1 + table_lines2

    # Iterate over each line in the table
    for line in table_lines:
        # Split the line by tabs ("\t") to separate the Trade and Links information
        elements = line.strip().split("\t")
        
        # Extract the trade name
        trade = elements[0]
        
        # Extract the links and convert them into a list
        links = elements[1:]
        
        # Store the trade and links information in the dictionary
        trade_links_dict[trade] = links

    
    Bist100_part1 = ['AEFES','AGHOL','AHGAZ','AKBNK','AKCNS','AKFYE','AKSA','AKSEN','ALARK','ALBRK','ALFAS','ARCLK','ASELS','ASGYO','ASTOR','BERA','BIENY','BIMAS','BIOEN','BOBET', \
            'BRSAN','BRYAT','BUCIM','CANTE','CCOLA','CIMSA','CWENE','DOAS','DOHOL','ECILC','ECZYT','EGEEN','EKGYO','ENERY','ENJSA','ENKAI','EREGL','EUPWR','EUREN','FROTO', \
            'GARAN','GESAN','GUBRF','GWIND','HALKB','HEKTS','IPEKE','ISCTR','ISDMR','ISGYO','ISMEN']

    Bist100_part2 = ['IZENR','IZMDC','KARSN','KAYSE','KCAER','KCHOL','KLSER','KMPUR','KONTR', \
            'KONYA','KORDS','KOZAA','KOZAL','KRDMD','MAVI','MGROS','MIATK','ODAS','OTKAR','OYAKC','PENTA','PETKM','PGSUS','QUAGR','SAHOL','SASA','SDTTR','SISE','SKBNK','SMRTG',\
            'SOKM','TATEN','TAVHL','TCELL','THYAO','TKFEN','TOASO','TSKB','TTKOM','TTRAK','TUKAS','TUPRS','ULKER','VAKBN','VESTL','YEOTK','YKBNK','YYLGD','ZOREN']

    #Bist100_part1 = ['FROTO']
    #Bist100_part2 = ['TCELL']

    #########  Creating web scrapping func. #########

    def web_scraping_1 (Bistlist):
        myuseragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--incognito")
        chromeOptions.add_argument(f"user-agent={myuseragent}")
        #chromeOptions.add_argument("--headless")
        browser = webdriver.Chrome(options=chromeOptions)
        df_part1 = pd.DataFrame(columns = ["Stock", "User", "Comment", "Comment Time"])

        for stock in Bistlist:
            for x in range(0,5):
                browser.get(trade_links_dict[stock][x])
                browser.delete_all_cookies()
                time.sleep(random.randint(2, 6))

                # Scroll to the middle of the page
                height = browser.execute_script("return document.documentElement.scrollHeight;")
                browser.execute_script(f"window.scrollTo(0, {height // 4});")
                time.sleep(random.randint(2, 4))

                # Scroll to the middle of the page
                height = browser.execute_script("return document.documentElement.scrollHeight;")
                browser.execute_script(f"window.scrollTo(0, {height // 1.4});")
                time.sleep(random.randint(2, 4))

                # Scroll to the end of the page
                browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
                source = browser.page_source
                soup = BeautifulSoup(source, "html.parser")
                metinler = soup.find_all("div",attrs={"class":"border-t border-[#E6E9EB]"})
                each_link = []

                for metin in metinler:
                    comment = metin.find("div", attrs={"class":"break-words leading-5"})
                    time_info = metin.find("span", attrs={"class":"text-[#5B616E]"})
                    user_info = metin.find("a", attrs={"class":"mb-1 font-bold hover:text-[#1256A0] hover:underline"})

                    if comment:
                        comment_ = comment.text
                        comment_time = time_info.text
                        user = user_info.text
                        each_link.append([stock, user, comment_, comment_time])

                df = pd.DataFrame(each_link, columns = ["Stock", "User", "Comment", "Comment Time"])
                df_part1 = pd.concat([df_part1, df], ignore_index=True)

                time.sleep(random.randint(2, 6))

                # if there are some comment which are not today, we'll not go further
                if not df["Comment Time"].str.contains("saat", case=False, na=False).any():
                    break
                x += 1
                
        browser.quit()
        df_part1.drop_duplicates(inplace=True)
        return df_part1


    def web_scraping_2 (Bistlist):
        myuseragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--incognito")
        chromeOptions.add_argument(f"user-agent={myuseragent}")
        #chromeOptions.add_argument("--headless")
        browser = webdriver.Chrome(options=chromeOptions)
        df_part2 = pd.DataFrame(columns = ["Stock", "User", "Comment", "Comment Time"])

        for stock in Bistlist:
            for x in range(0,5):
                browser.get(trade_links_dict[stock][x])
                browser.delete_all_cookies()
                time.sleep(random.randint(2, 6))

                # Scroll to the middle of the page
                height = browser.execute_script("return document.documentElement.scrollHeight;")
                browser.execute_script(f"window.scrollTo(0, {height // 4});")
                time.sleep(random.randint(2, 4))

                # Scroll to the middle of the page
                height = browser.execute_script("return document.documentElement.scrollHeight;")
                browser.execute_script(f"window.scrollTo(0, {height // 1.4});")
                time.sleep(random.randint(2, 4))

                # Scroll to the end of the page
                browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
                source = browser.page_source
                soup = BeautifulSoup(source, "html.parser")
                metinler = soup.find_all("div",attrs={"class":"border-t border-[#E6E9EB]"})
                each_link = []

                for metin in metinler:
                    comment = metin.find("div", attrs={"class":"break-words leading-5"})
                    time_info = metin.find("span", attrs={"class":"text-[#5B616E]"})
                    user_info = metin.find("a", attrs={"class":"mb-1 font-bold hover:text-[#1256A0] hover:underline"})

                    if comment:
                        comment_ = comment.text
                        comment_time = time_info.text
                        user = user_info.text
                        each_link.append([stock, user, comment_, comment_time])

                df = pd.DataFrame(each_link, columns = ["Stock", "User", "Comment", "Comment Time"])
                df_part2 = pd.concat([df_part2, df], ignore_index=True)

                time.sleep(random.randint(2, 6))

                # if there are some comment which are not today, we'll not go further
                if not df["Comment Time"].str.contains("saat", case=False, na=False).any():
                    break
                x += 1
                
        browser.quit()
        df_part2.drop_duplicates(inplace=True)
        return df_part2

    #########  Merge, Filter and Arrange Result #########

    def web_scraping_results ():
        df_part1 = web_scraping_1 (Bist100_part1)
        # filtering last 24 hours comments
        df_part1 = df_part1[df_part1["Comment Time"].str.contains("saat",case=False, na=False)]
        time.sleep(30)
        df_part2 = web_scraping_2 (Bist100_part2)
        # filtering last 24 hours comments
        df_part2 = df_part2[df_part2["Comment Time"].str.contains("saat",case=False, na=False)]
        
        df_final = pd.concat([df_part1, df_part2], ignore_index=True)
        return df_final

    # Getting result
    df_final = web_scraping_results()

    # Getting result 2
    # Add 'Date' column as the first column
    today_date = datetime.today().strftime('%Y-%m-%d')
    df_final["Date"] = today_date
    
    # Lowercase
    df_final["Comment"] = df_final["Comment"].apply(lambda x: " ".join(x.lower() for x in x.split()))

    # Translation dictionary for Turkish to English characters
    translation_dict = {
        'ı': 'i',
        'ğ': 'g',
        'ü': 'u',
        'ş': 's',
        'ö': 'o',
        'ç': 'c',
        'İ': 'I',
        'Ğ': 'G',
        'Ü': 'U',
        'Ş': 'S',
        'Ö': 'O',
        'Ç': 'C'
    }

    def translate_turkish_to_english(text):
        return text.translate(str.maketrans(translation_dict))
    df_final["Comment"] = df_final["Comment"].apply(translate_turkish_to_english)
    df_final["User"] = df_final["User"].apply(translate_turkish_to_english)
    df_final["Comment Time"] = df_final["Comment Time"].apply(translate_turkish_to_english)

    # Function to remove punctuation
    def remove_punctuation(text):
        return re.sub(r'[^\w\s]', '', text)
    df_final["Comment"] = df_final["Comment"].apply(remove_punctuation)
    
    # Convert DataFrame to JSON
    json_df_final = df_final.to_json(orient='records')

    # Define output folder-1
    output_folder = "daily_comments"
    # Create folder if it doesn't exist
    todate = datetime.today().date()
    folder_path = os.path.join(output_folder, str(todate))
    os.makedirs(folder_path, exist_ok=True)
    json_file_name = f"bist_comments_{todate}.json"
    output_path = os.path.join(folder_path, json_file_name)

    # Parse JSON string
    parsed_json_df_final = json.loads(json_df_final)

    # Write JSON to file without escape characters
    with open(output_path, 'w') as json_file:
        json.dump(parsed_json_df_final, json_file, indent=4)

    file_path = f"daily_comments/{todate}/bist_comments_{todate}.json"
    folder_name = f"bist_comments/"

    upload_to_s3(file_path, folder_name)