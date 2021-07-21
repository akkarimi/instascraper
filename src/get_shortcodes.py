import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import os
from bs4 import BeautifulSoup



fil = open("../data/shortcodes.txt","w")

def get_shortcode(driver, shortcode, fil):
	plain_text = driver.page_source
	soup = BeautifulSoup(plain_text, "html.parser")
	res = soup.find_all("a", href=True)
	length = len(res)
	for i in range(length):
		code = res[i]['href']
		if code.startswith("/p/") and code not in shortcode:
			shortcode.append(code)
			fil.write(code + '\n')
			print(code)


driver = webdriver.Chrome(executable_path='/home/ak/chromedriver/chromedriver')
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(60)
driver.get("https://www.instagram.com/adidasoriginals/?hl=en")
time.sleep(5)
elem = driver.find_element_by_tag_name("body")
no_of_pagedowns = 50

shortcode = []


while True:
	elem.send_keys(Keys.PAGE_DOWN)
	time.sleep(1)
	get_shortcode(driver, shortcode, fil)
	no_of_pagedowns-=1

print(len(shortcode))

fil.close()
