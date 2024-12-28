import time
import urllib
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

proxy_username = "aditya3356"
proxy_password = "TheUltimateStrongestWord@789"
proxy_host = "in.proxymesh.com"
proxy_port = "31280"
proxy_url = f"{proxy_host}:{proxy_port}"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

MONGO_URI = "mongodb+srv://Nikunj:" + urllib.parse.quote("TheUltimateStrongestWord@789") + "@stirassignment.fmyer.mongodb.net/?retryWrites=true&w=majority&appName=STIRASSIGNMENT"
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client['stir_db']
collection = db['trending_topics']

def create_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def enter_password(driver):
    print("Entering password")
    driver.find_element(By.NAME, "password").send_keys("TheUltimateStrongestWord@789")
    driver.find_element(By.XPATH, "//button[@data-testid='LoginForm_Login_Button']").click()
    time.sleep(5)

def scrape_trending_topics():
    try:
        print("Creating Selenium driver")
        driver = create_driver()

        print("Opening URL https://x.com/i/flow/login")
        driver.get("https://x.com/i/flow/login")
        time.sleep(20)

        print("Entering username")
        driver.find_element(By.NAME, "text").send_keys("Nikunj3356")
        driver.find_elements(By.TAG_NAME, "button")[3].click()
        time.sleep(5)

        if (len(driver.find_elements(By.NAME, "password"))!=0):
            enter_password(driver)
        else:
            print("Entering email ID")
            driver.find_element(By.NAME, "text").send_keys("nikunj.3356@gmail.com")
            driver.find_elements(By.TAG_NAME, "button")[2].click()
            time.sleep(5)
            enter_password(driver)

        print("Opening URL https://x.com/explore/tabs/trending")
        driver.get("https://x.com/explore/tabs/trending")
        time.sleep(10)

        print("Fetching top 5 trending topics")
        trend_elements = driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
        
        trends = []
        for i in range(5):
            trend_name = trend_elements[i].text.split('\n', 4)[3]
            trends.append(trend_name)

        print("Opening URL http://google.com")
        ip_address = requests.get('http://google.com', proxies=proxies).headers['X-ProxyMesh-IP']

        results = {
            'date_time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'ip_address': ip_address,
            'trend1': trends[0],
            'trend2': trends[1],
            'trend3': trends[2],
            'trend4': trends[3],
            'trend5': trends[4]
        }

        print("Storing the results in MongoDB")
        collection.insert_one(results)

        return results
    except Exception as e:
        raise e
    finally:
        print("Quitting Selenium driver")
        driver.quit()
