import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

urls = ["https://buff.163.com/goods/921379?from=market#tab=", "https://buff.163.com/goods/900464?from=market#tab=", 
        "https://buff.163.com/goods/781534?from=market#tab=", "https://buff.163.com/goods/857515?from=market#tab=",
        "https://buff.163.com/goods/886606?from=market#tab=", "https://buff.163.com/goods/45237?from=market#tab=",
        "https://buff.163.com/goods/769121?from=market#tab=", "https://buff.163.com/goods/35086?from=market#tab=",
        "https://buff.163.com/goods/38148?from=market#tab=", "https://buff.163.com/goods/763236?from=market#tab=",
        "https://buff.163.com/goods/779175?from=market#tab=",  "https://buff.163.com/goods/37510?from=market#tab=",
        "https://buff.163.com/goods/35883?from=market#tab=", "https://buff.163.com/goods/33820?from=market#tab=",
        "https://buff.163.com/goods/34989?from=market#tab=", "https://buff.163.com/goods/871092?from=market#tab=",
        "https://buff.163.com/goods/35895?from=market#tab=", "https://buff.163.com/goods/33813?from=market#tab=",
        "https://buff.163.com/goods/38150?from=market#tab=", "https://buff.163.com/goods/773524?from=market#tab=",
        "https://buff.163.com/goods/36354?from=market#tab=", "https://buff.163.com/goods/33825?from=market#tab=",
        "https://buff.163.com/goods/759175?from=market#tab=", "https://buff.163.com/goods/35893?from=market#tab=",
        "https://buff.163.com/goods/34369?from=market#tab=", "https://buff.163.com/goods/35885?from=market#tab=",
        "https://buff.163.com/goods/34987?from=market#tab=", "https://buff.163.com/goods/774681?from=market#tab=",
        "https://buff.163.com/goods/35890?from=market#tab=", ]
driver = webdriver.Chrome()

def find_selling_price(url):
    url += "selling"
    driver.get(url)

    # Wait for the table to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div[5]/table/tbody/tr[2]/td[6]/a'))
    )

    # Find the <tr> elements based on class and data-orderid
    tr_elements = driver.find_elements(By.XPATH, '/html/body/div[6]/div/div[5]/table/tbody/tr[2]/td[6]/a')

    if tr_elements:
        min_sell = tr_elements[0].get_attribute("data-price")
        name = tr_elements[0].get_attribute("data-goods-name")
        print(name)
        return name, float(min_sell)
    else:
        print("No selling price found.")
        return None, None

def find_buying_price(url):
    url += "buying"
    driver.get(url)

    # Wait for the table to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div[5]/table/tbody/tr[2]/td[7]/a'))
    )

    buy_btn = driver.find_elements(By.XPATH, '/html/body/div[6]/div/div[5]/table/tbody/tr[2]/td[7]/a')
    
    if buy_btn:
        min_buy = buy_btn[0].get_attribute("data-price")
        return float(min_buy)
    else:
        print("No buying price found.")
        return None

def check_arbitrage(name, selling_price, buying_price):
    arbitrage = buying_price - selling_price - (0.025 * buying_price)
    print(f"arbitrage found: possible profit- {arbitrage}")  
    if arbitrage > 0:
        print("DING DONG")
        record_arbitrage(name, arbitrage)

def record_arbitrage(name, arbitrage):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("records.txt", "a") as file:
        file.write(f"{timestamp} - {name}: Arbitrage - {arbitrage}\n")

while True:
    try:
        for url in urls:
            name, min_sell = find_selling_price(url)
            min_buy = find_buying_price(url)
            print("Min Selling:", min_sell)
            print("Min Buying:", min_buy)
            if name and min_buy:
                check_arbitrage(name, min_sell, min_buy)
            print("________________________________________________")
        print("FINISH")
        time.sleep(30)

    except Exception as e:
        print(e)
        time.sleep(30)

driver.quit()