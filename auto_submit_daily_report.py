from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from time import sleep

options = ChromeOptions()

# options.add_argument('--headless')

# driver = Chrome(options=options)
driver = Chrome()
# driver.get('http://maker.usoko.net/nounai/')
# driver.find_element_by_name('oo').send_keys('たかし')
# driver.find_element_by_xpath('//*[@id="con_main"]/form/input[3]').click()

driver.get('https://www.google.co.jp/')
query_text = driver.find_element_by_name('q')
query_text.send_keys('selenium python')
query_text.send_keys(Keys.ENTER)

# assert 'Google' in driver.title

sleep(5)

driver.quit()

print('hoge')
