from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import math
from data_cleaning import cleaning

# Chrome drive setup
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('headless')
s = Service(r"C:\Users\kacpe\OneDrive\Pulpit\Python\Projekty\chromedriver.exe")
url = "https://polygonscan.com/token/0x64a795562b02830ea4e43992e761c96d208fc58d"
driver = webdriver.Chrome(service=s, options=options)
driver.get(url)

# Cookies
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button#btnCookie"))
).click()

# Locate number of total transfer to check how many pages have table
num_trans = driver.find_element(By.XPATH, '//*[@id="totaltxns"]').text
num_trans = int(num_trans)
num = math.ceil(num_trans / 25)


# Switch to frame with NC transaction table
WebDriverWait(driver, 20).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#tokentxnsiframe")
    )
)

# Switch data format in table
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a#lnkTokenTxnsAgeDateTime"))
).click()

df = pd.DataFrame()
for _ in range(num):
    # Select data from table
    data = (
        WebDriverWait(driver, 20)
        .until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "table.table.table-md-text-normal")
            )
        )
        .get_attribute("outerHTML")
    )
    # Save to DataFrame
    if not df.empty:
        df_temp = pd.read_html(data)[0]
        df = df.append(df_temp).reset_index(drop=True)
    else:
        df = pd.read_html(data)[0]

    # Click to next page
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="maindiv"]/div[1]/nav/ul/li[4]'))
    ).click()

# Save to csv
df.to_csv(r"C:\Users\kacpe\OneDrive\Pulpit\Python\Projekty\nc-coin\app\transaction_history.csv")

# Clean data and save to csv
# cleaning('transaction_history.csv')
