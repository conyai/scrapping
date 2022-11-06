from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_attributes(driver, element) -> dict:
    return driver.execute_script(
        """
        let attr = arguments[0].attributes;
        let items = {}; 
        for (let i = 0; i < attr.length; i++) {
            items[attr[i].name] = attr[i].value;
        }
        return items;
        """,
        element
    )

# Путь к драйверу Chrome
driver = webdriver.Chrome(executable_path='D:\\soul\\sel\\chromeDriver\\chromedriver.exe')
options = webdriver.ChromeOptions()

class GoogleSheet:
    # ID Таблицы
    SPREADSHEET_ID = '1A8A6OKaSy--nOkeiNRmIj0n858EcT-OwhopjMvbuzvo'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

        
def main():
    gs = GoogleSheet()
    coin = 2
    try:
        domen = 'https://hotline.ua'
        # URL'ы категорий
        urls = ['/av/televizory/',]
        for url in urls:
            driver.get(domen+url)
            time.sleep(1)

            pagen_last = int(driver.find_elements(By.XPATH, '//a[@class="page"]')[-1].text)
            
            for i in range(1, pagen_last+1):
                driver.get(domen+url+f'?p={i}')

                driver.execute_script(f"window.scrollTo({0}, {2000})")
                time.sleep(2)
                prod_links_raw = driver.find_elements(By.XPATH, '//a[@class="list-item__title text-md"]')
                prod_links = []

                for prod_link_raw in prod_links_raw:
                    prod_links.append(prod_link_raw.get_attribute("href"))
                #print(len(prod_links))
                for prod_link in prod_links[]:
                    driver.get(prod_link+"?tab=about")
                    time.sleep(1)

                    sheets_range = f'Товары ХЛ!D{coin}:BC{coin}'
                    sheets_values = [[]]

                    # Тип товара
                    try:
                        type_XL = driver.find_elements(By.XPATH, '//span[@class="specifications-list__item"]')[0].text
                        sheets_values[0].append(type_XL)
                    except Exception:
                        sheets_values[0].append('')

                    # Брэнд
                    try:         
                        brand = driver.find_elements(By.XPATH, '//td[@data-v-6a24e12e=""]')[1].text
                        sheets_values[0].append(brand)
                    except Exception:
                        sheets_values[0].append('')

                    # Модель
                    try:
                        model = driver.find_elements(By.XPATH, '//td[@data-v-6a24e12e=""]')[3].text
                        sheets_values[0].append(model)
                    except Exception:
                        sheets_values[0].append('')

                    sheets_values[0].append(f'=TRIM(JOIN(" ";E{coin}:F{coin}))')
                    
                    # Цены
                    driver.get(prod_link)
                    prices = driver.find_elements(By.XPATH, '//span[@class="price__value"]')
                    prices_sheet = set()
                    for price in prices:
                        prices_sheet.add(price.text)
                    prices_sheet = list(prices_sheet)[1:]
                    prices_sheet = list(map(lambda x: int(x.replace(' ', '')), prices_sheet))

                    prices_sheet.sort()

                    for i in range(18):
                        try:
                            sheets_values[0].append(str(prices_sheet[i]))
                        except Exception:
                            sheets_values[0].append('')

                    driver.get(prod_link+'?tab=about')
                    # Фото
                    photos_srcs_raw = driver.find_elements(By.XPATH, '//img[@class="zoom-gallery__nav-img "]')
                    photos_srcs = []

                    for photo_src_raw in photos_srcs_raw:
                        try:
                            temp = list(photo_src_raw.get_attribute("src"))[:-4]
                            last = temp.pop(-1)
                            temp.append(str(int(last)+2))
                            photos_srcs.append(''.join(temp)+'.jpg')
                        except Exception:
                            photos_srcs.append('')
                    
                    for i in range(3):
                        try:
                            sheets_values[0].append(photos_srcs[i])
                        except Exception:
                            sheets_values[0].append('')

                    # Список характеристик
                    character_sheet = []
                    but = driver.find_element(By.XPATH, '//div[@class="header__switcher-item flex middle-xs"]')
                    but.click()

                    chars_all = driver.find_elements(By.XPATH, '//tr[@data-v-6a24e12e=""]')
                    for i in range(2, 26):
                        character_sheet.append(chars_all[i].text.replace('\n', ' ').replace('?', ' '))


                    for i in range(23):
                        if character_sheet[i]:
                            sheets_values[0].append(character_sheet[i])
                        else:
                            sheets_values[0].append('')

                    # Категория и две подкатегории
                    cats = driver.find_elements(By.XPATH, '//li[@class="breadcrumbs__item"]')
                    try:
                        category = cats[1].text
                        sheets_values[0].append(category)
                    except Exception:
                        sheets_values[0].append('')

                    try:
                        subcategory1 = cats[2].text
                        sheets_values[0].append(subcategory1)
                    except Exception:
                        sheets_values[0].append('')

                    try:
                        subcategory2 = cats[3].text
                        sheets_values[0].append(subcategory2)
                    except Exception:
                        sheets_values[0].append('')

                    sheets_values[0].append(f'=TRIM(JOIN(" > ";AZ{coin}:BB{coin}))')
                    gs.updateRangeValues(sheets_range, sheets_values)
                    coin += 1
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()