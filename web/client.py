from selenium import webdriver
from config import settings
import time
from process_parser import High, Down

driver = webdriver.Chrome(executable_path=settings.get('CHROME_DRIVER', default=None))  # Optional argument, if not specified will search path.
driver.get(settings.get('URL_BASE') + settings.get('URL_IBOV'))
time.sleep(1)

page_high = driver.page_source
High.top_five(page_high)

low = driver.find_element_by_xpath("//a[@href='#asDown']")
low.click()
time.sleep(1)

page_down = driver.page_source
Down.top_five(page_down)


#time.sleep(5)
driver.quit()
