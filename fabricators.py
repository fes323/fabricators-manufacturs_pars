import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


proxy = ''
options = Options()
options.add_argument(f'--proxy-server={proxy}')
options.add_argument('--window-size=2560,1440')


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)

detail_urls = []
first_page = True
page = 1
while True:
    time.sleep(random.randint(0, 4))

    if first_page:
        driver.get(f'https://fabricators.ru/produkt/toplivo')
        first_page = False
    else:
        driver.get(f'https://fabricators.ru/produkt/toplivo?page={page}')

    cards = driver.find_elements(By.CLASS_NAME, 'content-list-item')
    if len(cards) == 0:
        break

    for card in cards:
        detail_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
        detail_urls.append(detail_url)

    page += 1

data_list = []
for url in detail_urls:
    data = {}
    driver.get(url)

    company_title = driver.find_element(By.XPATH, '/html/body/div[1]/div/section[1]/div/div/div[2]/h1').text
    data['Название'] = company_title

    try:
        table_rq = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "section-st-block9"))
        )
        rows = table_rq.find_elements(By.CLASS_NAME, "content-contact-item")
        if len(rows) == 0:
            continue
        for row in rows:
            try:
                key = row.find_element(By.CLASS_NAME, "content-contact-item__tt").text.strip()
            except:
                continue
            try:
                value = row.find_element(By.CLASS_NAME, "content-contact-item__block").text.strip()
            except:
                continue
            finally:
                if key in data:
                    data[key].append(value)
                else:
                    data[key] = value
    except:
        pass


    try:
        table_data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "section-st-block5"))
        )
        rows = table_data.find_elements(By.CLASS_NAME, "content-contact-item")
        if len(rows) == 0:
            continue
        for row in rows:
            try:
                key = row.find_element(By.CLASS_NAME, "content-contact-item__tt").text.strip()
            except:
                continue
            try:
                value = row.find_element(By.CLASS_NAME, "content-contact-item__block").text.strip()
            except:
                continue
            finally:
                if key in data:
                    data[key].append(value)
                else:
                    data[key] = value
    except:
        continue
    if len(data) > 1:
        data_list.append(data)


driver.quit()

df = pd.DataFrame(data_list)
with pd.ExcelWriter('catalog-produkty-pitaniia-45.xlsx') as writer:
    df.to_excel(writer)