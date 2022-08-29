#from ast import Delete
import csv
#from distutils.log import error
#from lib2to3.pgen2 import driver
#from mailbox import NoSuchMailboxError
#from math import nextafter
#from subprocess import TimeoutExpired
#from textwrap import indent
#from timeit import repeat
#from tokenize import Ignore
#from unicodedata import name
from urllib import response
from winreg import DeleteValue
#from psycopg2 import ProgrammingError
import time
#from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
#from urllib3 import Timeout



browser = webdriver.Chrome()
url = "https://lardi-trans.com/uk/reliability_zone/raiting/ua/?sort=point&ustatus=carrier"
browser.get(url)
time.sleep(2)

login_input = browser.find_element_by_css_selector("body > main > div > div > form > div:nth-child(2) > div > div > input")
login_input.clear()
login_input.send_keys("Soltan.seryozha")
time.sleep(2)

password_input = browser.find_element_by_css_selector("body > main > div > div > form > div:nth-child(3) > div > div > input")
password_input.clear()
password_input.send_keys("data04")
time.sleep(2)
password_input.send_keys(Keys.ENTER)
time.sleep(2)
#browser.find_element_by_css_selector("body > div.wrapper.main-page > div.layout-content.container-main > div > div > div.lrd-ui--firm-rating__filters > div:nth-child(1) > select > option:nth-child(3)").click()
with open("Перевізники.csv", "a", encoding="UTF-8") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(
        (
            "Название компании",
            "Место регистрации",
            "Email",
            "Телефон"
        )
    )

for i in range(1, 51):
	browser.switch_to.window(browser.window_handles[0])
	browser.get(url + f'&page={i}')
	#browser.switch_to.window(browser.window_handles[0])
	time.sleep(2)
	names = browser.find_elements_by_xpath("//a[@rel='noreferrer']")
	print(len(names))
	for j in range(18):
		browser.switch_to.window(browser.window_handles[0])
		time.sleep(3)
		names[j].click()
		time.sleep(2)
		browser.switch_to.window(browser.window_handles[1])
		time.sleep(2)
		profile = browser.find_element_by_xpath("//a[@data-link='contacts']")
		profile.click()

		try:
			namef = browser.find_element_by_class_name("firm__description__title").text
			phones = browser.find_element_by_class_name("firm__contact__phone").text
			email = browser.find_element_by_css_selector("#firm__tab__contacts > section > div.firm__contacts__main-contacts-wrapper > div:nth-child(1) > div.firm__contacts__main-contact-info > div.firm__contacts__main-contact-send.firm__contact__icon.firm__contact__icon_mail > div > div").get_attribute("data-email")
			gps = browser.find_element_by_class_name("firm__contacts__main-contacts-address__info__top").text
		except NoSuchElementException:
			DeleteValue
		try:
			with open('Перевізники.csv', 'a', encoding='utf-8') as file:
				writer = csv.writer(file, delimiter=',')
				writer.writerow(
					(namef, gps, email, phones)
					)
		except NameError:
			browser.close()
			continue
		browser.close()


