import pandas as pd
import dou
from login import login, password


url = 'https://shop.vedes.com'
data = pd.read_excel('table.xlsx', index_col=0)
startpos = [1, 1]

def func() -> None:
	while startpos[0] < 8:
		startpos = dou.scraper(url=url, login=login, password=password, data=data, startpos=startpos)
	dou.scraper(url=url, login=login, password=password, data=data, startpos=startpos)
	df = pd.read_excel('table.xlsx', index_col=0)
	df = df.drop_duplicates()
	df.to_excel('result.xlsx')


def main() -> None:
	func()

if __name__ == '__main__':
	main()