from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random


with open('http_proxies.txt', 'r') as file:
	a = file.read()
	proxies = a.split('\n')

proxy = proxies[random.randrange(len(proxies))]

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36")

#options.headless = True
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument(f'--proxy-server={proxy}')
current_path = 'D:\\soul\\sel\\chromeDriver'
driverPath = str(current_path) + "\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driverPath, options=options)

def get_phone(url):
	try:
		driver.get(url)
		time.sleep(4)

		cook = driver.find_element(By.XPATH, "//button[@data-cy='dismiss-cookies-overlay']")
		cook.click()

		button = driver.find_element(By.XPATH, "//button[@data-testid='show-phone']")
		button.click()
		driver.implicitly_wait(4)

		numbers = driver.find_elements(By.XPATH, "//a[@data-testid='contact-phone']")
		numbers1 = []

		for i in numbers:
			numbers1.append(i.text)

		return(list(set(numbers1)))
	except Exception as ex:
		print(ex)
	finally:
		driver.close()
		driver.quit()

if __name__ == '__main__':
	phones = get_phone('https://www.olx.ua/d/obyavlenie/prodam-prostornuyu-2kk-na-3-slobodskoy-chkalova-IDOIrsb.html')
	print('-'*100)
	print(phones)