from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())

def scroll():
    """
    스크롤하지 않으면 나타나지 않는 재생목록이 있기 때문에, 스크롤하는 함수 생성
    """
    try:        
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            pause_time = random.uniform(1, 2)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(pause_time)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break
            else:
                last_page_height = new_page_height
            
    except Exception as e:
        print("에러 발생: ", e)

driver = webdriver.Chrome(service=service)

URL = "https://www.youtube.com/playlist?list=PLgvhB6TRB-zbVDEDbFM2jjoEda9iqY7AR"
driver.get(URL)
time.sleep(3)
scroll()

html_source = driver.page_source
soup_source = BeautifulSoup(html_source, 'html.parser')

content_total = soup_source.find_all('a','yt-simple-endpoint style-scope ytd-playlist-video-renderer')
content_title = list(map(lambda data: data.get_text().replace("\n", "").strip(), content_total))
content_link = list(map(lambda data: data["href"], content_total))

content_total_dict = {'title':content_title, 
                      'url':content_link,
                     }

data_save = pd.DataFrame(content_total_dict)

data_save.to_csv("28.csv", encoding='utf-8-sig')