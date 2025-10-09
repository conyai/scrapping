import time
import random
import numpy as np 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from login import login, password


url = 'https://shop.vedes.com'
data = pd.read_excel('table.xlsx', index_col=0)
startpos = [1, 1]

def scraper(data, startpos, url, login, password) -> list:
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0")

	#options.headless = True
	#options.add_argument("--disable-blink-features=AutomationControlled")

	current_path = 'D:\\scrapers\\doutch'
	driverPath = str(current_path) + "\\chromedriver.exe"

	driver = webdriver.Chrome(executable_path=driverPath, options=options)
	driver.implicitly_wait(15)

	try:
		driver.get(url)
		time.sleep(2)

		login_input = driver.find_element(By.XPATH, '//input[@id="username"]')
		login_input.clear()
		login_input.send_keys(str(login))
		time.sleep(2)

		password_input = driver.find_element(By.XPATH, '//input[@id="password"]')
		password_input.clear()
		password_input.send_keys(str(password))
		time.sleep(2)
		password_input.send_keys(Keys.ENTER)
		time.sleep(4)

		cookies = driver.find_element(By.XPATH, '//*[text()="Alle Akzeptieren"]')
		cookies.click()
		time.sleep(2)

		products = driver.find_element(By.XPATH, '//*[text()="Produkte"]')
		products.click()
		time.sleep(5)

		pos = [0, 0]

		urls = ['https://shop.vedes.com/b2b/de/10000/', 'https://shop.vedes.com/b2b/de/80000/', 'https://shop.vedes.com/b2b/de/160000/', 'https://shop.vedes.com/b2b/de/250000/', 'https://shop.vedes.com/b2b/de/360000/', 'https://shop.vedes.com/b2b/de/460000/', 'https://shop.vedes.com/b2b/de/570000/', 'https://shop.vedes.com/b2b/de/680000/', 'https://shop.vedes.com/b2b/de/1130000/']

		position = startpos[1]
		for url1 in urls[startpos[0]:]:
			pos[0] = urls.index(url1)
			driver.get(url1)
			time.sleep(2)

			try:
				view = driver.find_element(By.XPATH, '//label[@for="page_view_changer-list-view"]')
				view.click()
			except Exception:
				pass
			time.sleep(2)

			lis = driver.find_elements(By.XPATH, '//li[@class="page-item"]')
			maxx = lis[-2].text
			for i in range(position, int(maxx)+1):
				pos[1] = i
				driver.get(url1 + f'page{i}')
				time.sleep(2)

				
				forms = driver.find_elements(By.XPATH, '//form[@name="form_itemlist_"]')
				if len(forms) == 0:
					break
				print(len(forms))
				for form in forms:
					ean = form.find_elements(By.XPATH, './/div[@class="itemcard_list__article_attributes--entry"]')[3].find_elements(By.TAG_NAME, 'span')[1].text
					try:
						price = form.find_element(By.XPATH, './/div[@class="priceWrapper"]').text
					except Exception:
						price = ''
					data.loc[len(data)] = [str(ean), str(price)]
					print(str(ean), str(price), 'added to dataframe')
					print('length of df ',len(data))
				position = 1


		
	except Exception as ex:
		pass
	finally:
		driver.close()
		driver.quit()
		return pos
	data.to_excel('table.xlsx')

def main() -> None:
	scraper(data=data, startpos=startpos, url=url, login=login, password=password)


if __name__ == '__main__':
	main()