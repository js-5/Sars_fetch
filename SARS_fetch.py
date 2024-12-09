from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import requests
def click_with_retries(driver, by, value, retries=5, delay=2):
    for attempt in range(retries):
        try:
            element = driver.find_element(by, value)
            element.click()
            print("Element clicked successfully.")
            time.sleep(delay)
            return
        except NoSuchElementException:
            print(f"Attempt {attempt + 1}: Element not found, retrying...")
            time.sleep(delay)
    print("Failed to click element after retries.")

url = 'https://tools.sars.gov.za/tradestatsportal/data_download.aspx'
response = requests.get(url)
try:
    if response.status_code == 200:
        for i in range(2):
            print("Page available. Proceeding with Selenium.")
            driver = webdriver.Chrome(service=Service())
            driver.get('https://tools.sars.gov.za/tradestatsportal/data_download.aspx')
            time.sleep(2)
            if i == 0:
                tradePath = "//input[@type='radio' and @value='rdbExports']"  #Selects Trade category
            else:
                tradePath = "//input[@type='radio' and @value='rdbImports']"
            click_with_retries(driver,By.XPATH,tradePath)
            click_with_retries(driver,By.CSS_SELECTOR,"input[type='radio'][value='rdbCountries']")
            click_with_retries(driver,By.XPATH, "//*[@id='caption0']")                                     #Dropdowns after selecting Countries and Trade
            click_with_retries(driver,By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[6]/td[2]/div/div[2]/div/span[1]/input")
            click_with_retries(driver,By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td")
            click_with_retries(driver,By.XPATH, "//*[@id='caption1']")
            click_with_retries(driver,By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[8]/td[2]/span/div/div[2]/div/span[1]/input")
            click_with_retries(driver,By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td")
            click_with_retries(driver,By.XPATH, "//*[@id='caption3']")
            current_year = datetime.now().year
            target_year = current_year -2010
            current_month = datetime.now().month
            target_month = current_month - 3
            if target_month <= 0:  # If the month is January, February, or March
                target_month += 12
                target_year -= 1 
            xpath_year = f"//*[@id='ctl00_ContentPlaceHolder1_ddlYears_{target_year}']"
            click_with_retries(driver,By.XPATH, xpath_year,5,2)
            click_with_retries(driver,By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td")
            click_with_retries(driver,By.XPATH, "//*[@id='caption4']")
            month_xpath = f"//*[@id='ctl00_ContentPlaceHolder1_ddlMonths_{target_month}']"
            click_with_retries(driver,By.XPATH, month_xpath)
            click_with_retries(driver,By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td")
            click_with_retries(driver,By.XPATH,"//*[@id='ctl00_ContentPlaceHolder1_chkAll']")
            click_with_retries(driver,By.XPATH,"//*[@id='ctl00_ContentPlaceHolder1_btnDownload']",2,2)
            time.sleep(90)       #Substantial wait time to account for large files or slow connection to page
            driver.quit()
            with open("sars_fetch_log.txt","a") as file:
                if i == 0:
                    file.write(f"exports of {datetime.now().year}/{datetime.now().month -2} was logged at {datetime.today().strftime('%Y-%m-%d')}")
                else:
                    file.write(f"imports of {datetime.now().year}/{datetime.now().month -2} was logged at {datetime.today().strftime('%Y-%m-%d')}")
            file.close()
    else :
        print("Page could not be reached.")
        with open("sars_fetch_log.txt","a") as file:
            file.write(f"Page could not be reached at {datetime.today().strftime('%Y-%m-%d')}")
        file.close()
except Exception as e:
    print(f"Error:{e}")
