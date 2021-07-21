from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from langdetect import detect
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_comments(driver, address, line, doc_num):
    posts = open('../data/comments/' + line, 'w')
    driver.get(address)
    plain_html = click_load(driver)
    soup = bs(plain_html, 'html.parser')
    comments = soup.find_all('li', {'class':'gElp9'})
    encount = 0
    en_comments = []
    for i in range(len(comments)):
        if i == 0:
            continue
        res = comments[i]
        txt = res.find("span", {'class': ''}).text
        print(txt)
        try:
            if detect(txt) == 'en':
                en_comments.append(txt)

                posts.write(txt)
                posts.write('\n')
                encount = encount + 1
        except:
            pass
    # print(*en_comments, sep = '\n')

    print("%d --- English Comments in %s:" % (doc_num, line), len(en_comments))
    time.sleep(1)
    # driver.quit()
    posts.close()

def click_load(driver):
	# The XPATH for the button that loads more comments of the post. Copy from Inspect web page
    page_xpath = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button/span'
    html = driver.page_source
    while True:
        try:
        	driver.find_element(By.XPATH, page_xpath).click()
        except:
        	pass
        try:
        	WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, page_xpath)))
        except:
        	break
    html = driver.page_source
    return html


if __name__ == "__main__":
    shortcode_file = open('../data/shortcodes.txt','r')
    doc_num = 0
    driver = webdriver.Chrome(executable_path='/home/ak/chromedriver/chromedriver')
    time.sleep(30)
    for line in shortcode_file:
        address = 'https://www.instagram.com' + line
        get_comments(driver, address, line[3:-2], doc_num)
        doc_num = doc_num + 1
    shortcode_file.close()