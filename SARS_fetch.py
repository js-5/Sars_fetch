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
download_dir = "/Users/Jan/Documents/Test"  # Replace with your desired download path
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Change default download directory // does not work currently.
    "download.prompt_for_download": False,  # Disable the download prompt
    "download.directory_upgrade": True,  # Allow directory upgrade
    "safebrowsing.enabled": True  # Enable safe browsing
})
url = 'https://tools.sars.gov.za/tradestatsportal/data_download.aspx'
response = requests.get(url)
if response.status_code == 200:
    for i in range(2):
        print("Page available. Proceeding with Selenium.")
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        driver.get('https://tools.sars.gov.za/tradestatsportal/data_download.aspx')
        time.sleep(2)
        if i == 0:
            tradePath = "//input[@type='radio' and @value='rdbExports']"  #Selects Trade category
        else:
            tradePath = "//input[@type='radio' and @value='rdbImports']"
        driver.find_element(By.XPATH,tradePath ).click()
        time.sleep(0.15)
        driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='rdbCountries']").click()
        time.sleep(0.15)

        driver.find_element(By.XPATH, "//*[@id='caption0']").click()                                      #Dropdowns after selecting Countries and Trade
        time.sleep(0.15)
        driver.find_element(By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[6]/td[2]/div/div[2]/div/span[1]/input").click()
        time.sleep(0.15)
        driver.find_element(By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//*[@id='caption1']").click()
        time.sleep(0.15)
        driver.find_element(By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[8]/td[2]/span/div/div[2]/div/span[1]/input").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td").click()
        time.sleep(1.5)
        driver.find_element(By.XPATH, "//*[@id='caption3']").click()
        time.sleep(0.5)


        current_year = datetime.now().year
        target_year = current_year -2010
        current_month = datetime.now().month
        target_month = current_month - 3
        if target_month <= 0:  # If the month is January, February, or March
            target_month += 12
            target_year -= 1 
        xpath_year = f"//*[@id='ctl00_ContentPlaceHolder1_ddlYears_{target_year}']"
        driver.find_element(By.XPATH, xpath_year).click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//*[@id='caption4']").click()
        time.sleep(0.5)
        xpath = f"//*[@id='ctl00_ContentPlaceHolder1_ddlMonths_{target_month}']"
        try:
            driver.find_element(By.XPATH, xpath).click()
            print(f"Clicked on the dropdown for month: {target_month}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.5)
        driver.find_element(By.XPATH, "/html/body/form/center/table[2]/tbody/tr/td/div/div[2]/div[1]/table/tbody/tr[1]/td").click()
        time.sleep(0.15)
        driver.find_element(By.XPATH,"//*[@id='ctl00_ContentPlaceHolder1_chkAll']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@id='ctl00_ContentPlaceHolder1_btnDownload']").click()
        time.sleep(90)       #Substantial wait time to account for large files or slow connection to page
        driver.quit()
else :
    print("Page could not be reached.")

