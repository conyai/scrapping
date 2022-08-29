from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time


urls = [
	'https://opensea.io/explore-collections',
	'https://opensea.io/explore-collections?tab=top',
	'https://opensea.io/explore-collections?tab=art',
	'https://opensea.io/explore-collections?tab=collectibles',
	'https://opensea.io/explore-collections?tab=music',
	'https://opensea.io/explore-collections?tab=photography-category',
	'https://opensea.io/explore-collections?tab=sports',
	'https://opensea.io/explore-collections?tab=trading-cards',
	'https://opensea.io/explore-collections?tab=utility'
]

driver = webdriver.Chrome(executable_path='D:\\soul\\sel\\chromeDriver\\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36")

try:
	el = set()
	for url in urls:
		driver.get(url=url)
		er = 0
		for i in range(0, 100):
			page0 = driver.page_source
			driver.execute_script(f"window.scrollTo({1000*i}, {1000*i+1000})")
			page = driver.page_source
			if(page0 == page): 
				er += 1
			else:
				er = 0
			if(er == 5): break
			soup = BeautifulSoup(page, 'lxml')
			ass = soup.find_all('a', class_='sc-l6elh8-0 siFRp sc-1xf18x6-0 FNmrM AccountLink--ellipsis-overflow')
			for a in ass:
				d = 'https://opensea.io' + a.get('href')
				el.add(d)
			time.sleep(1.3)
	file = open('accounts.txt', 'w')
	file.write('\n'.join(el))
	file.close()
	print(f'Всего ссылок - {len(el)}')
except Exception as ex:
	print(ex)
finally:
	driver.close()
	driver.quit()
print('Выгрузка аккаунтов прошла успешно!')