from bs4 import BeautifulSoup
import requests
import os
import csv


url = 'https://prom.ua/ua/c2895199-olinua.html'

def _get(url):
	req = requests.get(url)
	src = req.text
	#with open('boss.html', 'w', encoding='utf-8') as file:
		#file.write(src)
	#with open('boss.html', 'r', encoding='utf-8') as src:
	hrefs = []

	soup = BeautifulSoup(src, 'lxml')
	for i in range(1, 31):
		href = soup.find('div', {'class':'kf2kF js-productad', 'data-position-qaid':f'{i}'}).find('a', {'target':'_self'}).get('href')
		href = href.split('?')[0]
		hrefs.append('https://prom.ua'+href)
		print(f'Ссылка на товар под номером {i} успешно сохранена')

	return hrefs


def photos(links):
	for lin in links:
		req = requests.get(lin)
		src = req.text
		soup = BeautifulSoup(src, 'lxml')
		
		if os.path.exists(f'data/t_{links.index(lin)+1}'):
			print('Folder is already exist')
		else:
			os.mkdir(f'data/t_{links.index(lin)+1}')

		try:
			limgs = soup.find('ul', class_='ND_Gc wYtre').find_all('li')
			for item in limgs:
				url = item.find('div', class_='NCAFH i6rXC O8pnz flK53 rJS7f').find('div', class_='NCAFH').find('img').get('src')
				resp = requests.get(url).content
				with open(f'data/t_{links.index(lin)+1}/{limgs.index(item)+1}.jpg', 'wb') as file:
					file.write(resp)
		except Exception:
			url = soup.find('div', {'data-qaid':'image_block'}).find('picture', class_='InqHo O6OJD').find('img').get('src')
			resp = requests.get(url).content
			with open(f'data/t_{links.index(lin)+1}/{limgs.index(item)+1}.jpg', 'wb') as file:
				file.write(resp)

		print(f'Фото товаров ссылки {links.index(lin)+1} успешно сохранены')


def desc(links):
	for link in links:
		req = requests.get(link)
		src = req.text
		soup = BeautifulSoup(src, 'lxml')
		inf = soup.find('div', {'data-qaid':"descriptions"}).text.strip()

		with open(f'data/t_{links.index(link)+1}/description.txt', 'w', encoding='utf-8') as file:
			file.write(inf)
		print(f'Описание {links.index(link)+1} товара успешно записано в файл')


def attributes(link):
	req = requests.get(link)
	print(req)
	src = req.text
	soup = BeautifulSoup(src, 'lxml')
	inf = soup.find('div', {'data-qaid':'attribute_block', 'class':'NCAFH chd9M urpUY vXWTQ NJEug ZR4VU UNDS2 _byRv vSs1A'}).find('div', class_='NCAFH vYTZ_ BdR0D').find(
		'ul', class_='ND_Gc TYx2q').find('li', class_='Kuaiv').find('ul', class_='ND_Gc wYtre').find_all('li')
	print(len(inf))
	#inf_all = []
	#for el in inf:
	#	i = []
	#	i.append(el.find('div', class_='kf2kF idp7J cxYWa Oz9HU').text)
	#	i.append(el.find('div', class_='kf2kF BQjDj').text)
	#	inf_all.append(i)

	#print(len(inf_all))

links = _get(url)
print(links[0])
#photos(links)
#desc(links)
attributes(links[0])