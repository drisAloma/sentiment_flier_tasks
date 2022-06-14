import pandas as pd
import numpy as np
import warnings
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

pd.set_option ('display.max_columns', None)
warnings.filterwarnings('ignore', category = FutureWarning)
warnings.filterwarnings('ignore', category = DeprecationWarning)

options = Options()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disabe-gpu")
options.add_argument("--no-sandbox")

def open(link):
    try:
        browser.get(link)
    except:
        print('no internet connection')

social = '//div[@class="is-flex mt-1 mb-2"]//a'
duration = '//div[@class="countdown is-flex-grow-1 is-flex-direction-column"]'
swapped = '//div[@class="is-flex is-align-items-center is-size-7"]'
progress_bar = '//div[@class="content-progress"]'

bar = []
website = []
twitter = []
facebook = []
telegram = []
presale_info= []
sales_window = []
sold =[]

def OpenProjectLink():
    open('https://www.pinksale.finance/?chain=BSC#/launchpads?chain=BSC')
    
    time.sleep(2)
    
    browser.maximize_window()
    time.sleep(10)
    
    a = browser.find_element(by = 'xpath', value ='//span[@class = "ant-select-selection-item"]')
    a.click()
    time.sleep(2)
    
    check = browser.find_element(by = 'xpath', value ='//div[@title = "Inprogress"]')
    check.click()
    time.sleep(10)
    
    global presale_info, website, twitter, facebook, telegram, status, sold, sales_window
    
    i=0
    while i < 6:
        try:
            browser.execute_script('window.scrollBy(0,120)','') # commit : added for more intervals
            time.sleep(2)
            i +=1
        except:
            break

    find_length = len(browser.find_elements(by = 'xpath', value ='//div[@class = "view-pool has-text-right"]//a[@class = "view-button"]'))
    
    progress = browser.find_elements(by = 'xpath', value = progress_bar)
    for val in progress:
        bar.append(val.text)
        
    time.sleep(2)
    
    period = browser.find_elements(by = 'xpath', value = duration)
    for val in period:
        sales_window.append(val.text)
    
    list_count = 0
    while (list_count < find_length):
        time.sleep(2)
        browser.execute_script('window.scrollBy(0,-1200)','') # commit : added for more intervals
        time.sleep(2)
        find = browser.find_elements(by = 'xpath', value ='//div[@class = "view-pool has-text-right"]//a[@class = "view-button"]')
        time.sleep(2)
        find[list_count].click()
        time.sleep(15)
        
        full_details = browser.find_elements(by = 'xpath', value = '//tbody//td')
        for detail in full_details:
            presale_info.append(detail.text)
            
        try:
            pool = browser.find_element(by = 'xpath', value = swapped)
            sold.append(pool.text)
        except:
            sold.append('Not Found')
            
        try:
            web_link = browser.find_elements(by = 'xpath', value = social)[0]
            website.append(web_link.get_attribute("href"))
        except:
            website.append('Not Available')
            
        try:
            twitter_link = browser.find_elements(by ='xpath', value = social)[1]
            twitter.append(twitter_link.get_attribute("href"))
        except:
            twitter.append('Not Available')
        
        try:
            facebook_link = browser.find_elements(by ='xpath', value = social)[2]
            facebook.append(facebook_link.get_attribute("href"))
        except:
            facebook.append('Not Available')
        
        try:
            telegram_link = browser.find_elements(by ='xpath', value = social)[3]
            telegram.append(telegram_link.get_attribute("href"))
        except:
            telegram.append('Not Available')
        time.sleep(2)
                           
        #go back
        browser.back()
        time.sleep(2)
        
        browser.execute_script('window.scrollBy(0,-1200)','')
        time.sleep(2)
        
        filter_ = browser.find_element(by = 'xpath', value ='//span[@class = "ant-select-selection-item"]')
        filter_.click()
        time.sleep(2)
        
        status = browser.find_element(by = 'xpath', value ='//div[@title = "Inprogress"]')
        status.click()
        time.sleep(2)
        
        i=0
        while i < 6: # commit : added for more intervals
            try:
                browser.execute_script('window.scrollBy(0,120)','')
                time.sleep(3)
                i+=1
            except:
                break
    
        if list_count == find_length-1:
            break
        list_count+=1
        
    return "Done"

browser = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe", options = options)
OpenProjectLink()

#Data cleaning/preprocessing

details = [re.sub('\\n(.*)','',item) for item in presale_info]

results = []
pattern = re.compile(r'^Presale.*(Address)$')
for detail in details:
    if pattern.match(detail):
        row = []
        results.append(row)
    row.append(detail)

lists = []
for k in range(len(results)):
    data = [val for i,val in enumerate(results[k]) if i%2 == 1]
    columns = [col for i,col in enumerate(results[k]) if i%2 == 0]
    dict_ = {columns[i]: data[i] for i in range(len(columns))}
    lists.append(pd.DataFrame(dict_, index = [0]))

dataframe = pd.concat(lists, axis= 0, ignore_index = True)

percent = [re.sub('\n.*','',item) for item in bar]
swapped_percent= [re.sub('^[a-zA-Z]*','',item) for item in percent]

sales_window = [re.sub('\n',' ',item) for item in sales_window]
sold = [re.sub('\n',' / ',item) for item in sold]

dataframe['swapped_percentage'] = swapped_percent
dataframe['token_sold'] = sold
dataframe['sales_window'] = sales_window
dataframe['website'] = website
dataframe['twitter'] = twitter
dataframe['telegram'] = telegram
dataframe['facebook'] = facebook

dataframe.to_csv('Pinksale_live.csv', index=False)