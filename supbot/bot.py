from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import keys
import time

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/Leo/Library/Application Support/Google/Chrome/User Data/")
browser = webdriver.Chrome('./chromedriver',options=options)
t = 1
ret_intval = 0.1


def isTheSame(element, keyDict, key, delim=None):
	enteredVal = element.get_attribute('value')
	if delim:
		enteredVal = "".join(enteredVal.split(delim))
	if enteredVal == keyDict[key]:
		return True
	return False

def sendAndCheck(element, keyDict, key, delim=None):
	if isTheSame(element, keyDict, key, delim):
		return
	done = False
	element.clear()
	while not done:
		element.send_keys(keyDict[key])
		if isTheSame(element, keyDict, key, delim):
			done = True
			return
		element.clear()
		time.sleep(ret_intval)

def getProductUrl(ckeys):
	browser.get('https://www.supremenewyork.com/shop/all/{}'.format(ckeys['category']))
	if ckeys['exact']:
		browser.find_element_by_link_text(ckeys['prodName']).click()
	else:
		browser.find_element_by_partial_link_text(ckeys['prodName']).click()
	time.sleep(1)

	if 'prodStyle' in ckeys:
		browser.find_element_by_xpath('//button[contains(@data-style-name, "{}")]'.format(ckeys['prodStyle'])).click()
		# browser.find_element_by_partial_link_text(ckeys['prodStyle']).click()
		time.sleep(1)
	if 'size' in ckeys:
		Select(browser.find_element_by_id('s')).select_by_visible_text(ckeys['size'])
	


def order(ckeys):

	browser.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()
	time.sleep(t)

	browser.get('https://www.supremenewyork.com/checkout')
	time.sleep(t)

	browser.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(ckeys['name'])
	time.sleep(t)

	browser.find_element_by_xpath('//*[@id="order_email"]').send_keys(ckeys['email'])
	time.sleep(t)

	telElem = browser.find_element_by_xpath('//*[@id="order_tel"]')
	sendAndCheck(telElem, ckeys, 'tel', delim='-')
	time.sleep(t)

	addrElem = browser.find_element_by_xpath('//*[@id="bo"]')
	sendAndCheck(addrElem, ckeys, 'address')
	time.sleep(t)

	if 'apt' in ckeys:
		browser.find_element_by_xpath('//*[@id="oba3"]').send_keys(ckeys['apt'])
		time.sleep(t)
	
	browser.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(ckeys['zip'])
	time.sleep(t)
	
	if 'zip' not in ckeys:
		cityElem = browser.find_element_by_xpath('//*[@id="order_billing_city"]')
		sendAndCheck(cityElem, ckeys, 'city')
		time.sleep(t)

	# Card info
	cnElem = browser.find_element_by_xpath('//*[@id="cnb"]')
	sendAndCheck(cnElem, ckeys, 'card_num', delim=' ')
	time.sleep(t)

	# cvvElem = browser.find_element_by_xpath('//*[@id="vval"]')
	# sendAndCheck(cvvElem, ckeys, 'cvv')
	# time.sleep(t)

	browser.find_element_by_xpath('//*[@id="credit_card_month"]/option[{}]'.format(ckeys['card_month'])).click()
	time.sleep(t)

	year_option = int(ckeys['card_year'])-2018
	browser.find_element_by_xpath('//*[@id="credit_card_year"]/option[{}]'.format(year_option)).click()
	time.sleep(t)


	# Term and conditions 
	# browser.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()
	# time.sleep(t)

	# Buy
	# browser.find_element_by_xpath('//*[@id="pay"]/input').click()
	# time.sleep(t)
	



if __name__ == '__main__':
	getProductUrl(keys)
	order(keys)

