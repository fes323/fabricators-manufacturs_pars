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
        driver.get(f'https://manufacturers.ru/companies/kotelnye')
        first_page = False
    else:
        driver.get(f'https://manufacturers.ru/companies/kotelnye?page={page}')

    cards = driver.find_elements(By.CSS_SELECTOR, '.sim-item')
    if len(cards) == 0:
        break

    for card in cards:
        if card.get_attribute('class') != 'sim-item':
            continue
        detail_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
        detail_urls.append(detail_url)

    page += 1

data_list = []
for url in detail_urls:
    data_dict = {}
    driver.get(url)

    company_title = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/h1').text
    data_dict['Название'] = company_title

    try:
        table_category = driver.find_element(By.ID, "category")
        rows = table_category.find_elements(By.CLASS_NAME, "w-tr")
        for row in rows:
            try:
                row_data = row.find_elements(By.CLASS_NAME, "w-td")
            except:
                continue
            try:
                key = row_data[0].text.strip()
                value = row_data[1].text.strip()
            except:
                continue
            finally:
                data_dict[key] = value
    except:
        pass


    try:
        table_company = driver.find_element(By.ID, "company")
        rows = table_company.find_elements(By.CLASS_NAME, "w-tr")
        for row in rows:
            try:
                row_data = row.find_elements(By.CLASS_NAME, "w-td")
            except:
                continue
            try:
                key = row_data[0].text.strip()
                value = row_data[1].text.strip()
            except:
                continue
            finally:
                data_dict[key] = value
    except:
        pass

    try:
        table_contact = driver.find_element(By.ID, "contact-list")
        rows = table_contact.find_elements(By.CLASS_NAME, "cont-tr")
        for row in rows:
            try:
                row_data = row.find_elements(By.CLASS_NAME, "cont-td")
            except:
                continue
            try:
                key = row_data[0].text.strip()
                value = row_data[1].text.strip()
            except:
                continue
            finally:
                data_dict[key] = value
    except:
        continue
    data_list.append(data_dict)


driver.quit()

df = pd.DataFrame(data_list)
with pd.ExcelWriter('kotelnye.xlsx') as writer:
    df.to_excel(writer)