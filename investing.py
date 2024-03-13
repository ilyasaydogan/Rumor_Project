def web_scraping_1 (Bistlist):

    myuseragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument(f"user-agent={myuseragent}")
    # chromeOptions.add_argument("--headless")
    browser = webdriver.Chrome(options=chromeOptions)
    start_time = time.time()
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

    # end_time = time.time()
    # execution_time = (end_time - start_time) / 60
    # print("web_scraping_1 Execution time:", round(execution_time, 2), "minutes")

    df_part1.drop_duplicates(inplace=True)
    return df_part1


def web_scraping_2 (Bistlist):

    myuseragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument(f"user-agent={myuseragent}")
    # chromeOptions.add_argument("--headless")
    browser = webdriver.Chrome(options=chromeOptions)
    start_time = time.time()
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

    # end_time = time.time()
    # execution_time = (end_time - start_time) / 60
    # print("web_scraping_2 Execution time:", round(execution_time, 2), "minutes")

    df_part2.drop_duplicates(inplace=True)
    return df_part2