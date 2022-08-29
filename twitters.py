from bs4 import BeautifulSoup
from selenium import webdriver
import time


urls = list()

with open('accounts.txt', 'r') as file:
	a = file.read()
	urls = a.split('\n')

urls = urls[33:]
driver = webdriver.Chrome(executable_path='D:\\soul\\sel\\chromeDriver\\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36")

try:
	for url in urls:
		file = open('twitter.txt', 'a')
		driver.get(url=url)
		page = driver.page_source
		soup = BeautifulSoup(page, 'lxml')
		if(soup.find('a', class_='sc-l6elh8-0 fpieog')):
			twit = soup.find_all('a', class_='sc-l6elh8-0 fpieog')
			for t in twit:
				if t.get('href')[8] == 't':
					file.write(t.get('href')+'\n')
		time.sleep(2)
except Exception as ex:
	print(ex)
finally:
	driver.close()
	driver.quit()