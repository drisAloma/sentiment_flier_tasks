#ssh idris_azure@20.91.211.205
#ssh lawal_azure@51.12.244.129
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
#options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

titles = []
token_info = []
vesting_schedule= []
presale_status = []
twitter = []
website = []
telegram = []

social = '//p[@class="inline-flex gap-5 justify-end my-4"]//a'

def open(link):
    try:
        browser.get(link)
    except:
        print('no internet connection')

def OpenProjectLink():
    open('https://gamefi.org/')
    
    time.sleep(2)
    
    browser.maximize_window()
    
    find_length = len(browser.find_elements(by = 'xpath', value ='//div[@class = "cursor-pointer"]/img'))
    
    list_count = 0
    
    while (list_count < find_length):
        global titles, token_info, vesting_schedule, presale_status
        
        find = browser.find_elements(by = 'xpath', value ='//div[@class = "cursor-pointer"]/img')
        find[list_count].click()
        
        time.sleep(5)
        
        try:
            title = browser.find_element(by ='xpath', value = '//h2[@class = "font-semibold text-2xl font-casual capitalize my-2"]').text
            titles.append(title)
        except:
            titles.append("Not Found")
        
        try:
            info = browser.find_elements(by ='xpath', value = '//div[@class = "flex justify-between mb-4 items-center"]')
            for element in info:
                token_info.append(element.text)
        except:
            info.append('TBD')
            
            
        try:
            vesting = browser.find_elements(by ='xpath', value = '//span[@class = "text-gamefiDark-100 text-[13px]"]')
            for detail in vesting:
                vesting_schedule.append(detail.text)
        except:
            vesting.append('TBD')
            
        try:
            web_link = browser.find_elements(by ='xpath', value = social)[0]
            website.append(web_link.get_attribute("href"))
        except:
            website.append('Not Available')

        try:
            telegram_link = browser.find_elements(by ='xpath', value = social)[1]
            telegram.append(telegram_link.get_attribute("href"))
        except:
            telegram.append('Not Available')

        try:
            twitter_link = browser.find_elements(by ='xpath', value = social)[2]
            twitter.append(twitter_link.get_attribute("href"))
        except:
            website.append('Not Available')

        try:
            stat_1 = browser.find_element(by ='xpath', value = '//div[@class = "inline-flex gap-1 items-center text-sm"]').text
            stat_2 = browser.find_element(by ='xpath', value = '//div[@class = "flex gap-2 lg:gap-4 items-center justify-center"]').text
            status = stat_1+' '+stat_2
            status = status.replace('\n',' ')
            presale_status.append(status)
        except:
            presale_status.append('COMING SOON')
        
        #go back
        browser.back()
        time.sleep(5)
        if list_count == find_length-1:
            break
        list_count +=1
        
    return "scrapped"

browser = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe", options = options)
OpenProjectLink()

info = [re.sub('.+[a-zA-Z]*\\n','',item) for item in token_info]
new_list = np.array(info).reshape(-1,7)

details =pd.DataFrame(new_list, columns = ['Symbol','Token Price','Total Raise','Swap Amount','Token Network',
                                        'IGO Network','Accepted Currency'])
details['Project Name'] = titles
details['Vesting Schedule'] = vesting_schedule
details['Launch Status']= presale_status
details['website'] = website
details['telegram'] = telegram
details['twitter'] = twitter

details =  details[['Project Name','Symbol','Token Price','Total Raise','Swap Amount','Token Network',
                    'IGO Network','Accepted Currency','Vesting Schedule','Launch Status','website',
                    'telegram','twitter']]

details.to_csv("GameFi_upcoming_launchpad.csv", index=False)
#dataframe = pd.read_csv("GameFi_upcoming_launchpad.csv")
#new_df = pd.concat([dataframe, details]).drop_duplicates()
#new_df.to_csv("GameFi_upcoming_launchpad.csv", index=False)


#ENDED PRESALES
card_details = []
titles = []
token_info = []
vesting_schedule= []
presale_status = []
twitter = []
website = []
telegram = []
swap_percent = []

#social = '//p[@class="inline-flex gap-5 justify-end my-4"]//a'
swap_progress= '//div[@class = "flex w-full justify-between font-casual text-[10px] text-white/50 mt-1"]'
next_btn = '//span[@class="inline-flex w-6 h-6 justify-center items-center rounded cursor-pointer border border-transparent"]'

def OpenProjectLink():
    open('https://gamefi.org/igo')
    time.sleep(2)
    browser.maximize_window()
    
    i=0
    while i<0:
        next_page=browser.find_elements(by = 'xpath', value = next_btn)
        next_page[1].click()
        time.sleep(2)
        i+=1
    time.sleep(5)
    
    global titles, card_details, token_info, vesting_schedule, presale_status, twitter, telegram, website, swap_percent
    
    try:
        cards = browser.find_elements(by="xpath", value='//div[@class="w-full flex flex-col gap-4 mt-12"]//div[@class="flex-1 flex-col"]')
        for value in cards:
            card_details.append(value.text)
    except:
        card_details.append('No Info')
    
    find_length = len(browser.find_elements(by = 'xpath', value ='//a[@class="hidden lg:block relative w-24 h-24 bg-black"]'))
    list_count = 0
    time.sleep(3)
    while (list_count < find_length):
        find = browser.find_elements(by = 'xpath', value ='//a[@class="hidden lg:block relative w-24 h-24 bg-black"]')
        time.sleep(2)
        find[list_count].click()
        time.sleep(2)
        click = browser.find_element(by = 'xpath', value ='//div[@class="tabs_menu__MkEqd text-base font-semibold"]')
        click.click()
        time.sleep(2)
        
        try:
            title = browser.find_element(by ='xpath', value = '//h2[@class = "font-semibold text-2xl font-casual capitalize my-2"]').text
            titles.append(title)
        except:
            titles.append("Not Found")
        
        try:
            info = browser.find_elements(by ='xpath', value = '//div[@class = "flex justify-between mb-4 items-center"]')
            for element in info:
                token_info.append(element.text)
        except:
            info.append('TBD')
            
        try:
            vesting = browser.find_elements(by ='xpath', value = '//span[@class = "text-gamefiDark-100 text-[13px]"]')
            for detail in vesting:
                vesting_schedule.append(detail.text)
        except:
            vesting.append('TBD') 
        
        try:
            swap = browser.find_element(by ='xpath', value = swap_progress)
            swap_percent.append(swap.text)
        except:
            vesting.append('TBD')
            
        try:
            web_link = browser.find_elements(by ='xpath', value = social)[0]
            website.append(web_link.get_attribute("href"))
        except:
            website.append('Not Available')

        try:
            telegram_link = browser.find_elements(by ='xpath', value = social)[1]
            telegram.append(telegram_link.get_attribute("href"))
        except:
            telegram.append('Not Available')

        try:
            twitter_link = browser.find_elements(by ='xpath', value = social)[2]
            twitter.append(twitter_link.get_attribute("href"))
        except:
            twitter.append('Not Available')
        
        #go back
        browser.back()
        time.sleep(6)
        if list_count == find_length-1:
            break
        list_count +=1
    return "scrapped"

browser = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe", options = options)
OpenProjectLink()

info = [re.sub('.+[a-zA-Z]*\\n','',item) for item in token_info]
new_list = np.array(info).reshape(-1,7)

status = [re.sub('\n','',item) for item in card_details]
next_claim = [re.sub('[a-zA-Z].*\w*(IN)','',item) for item in status]

percent = [re.sub('\n(.)*','',item) for item in swap_percent]

details = pd.DataFrame(new_list, columns = ['symbol','token_price','total_raise','swap_amount','token_network',
                                        'IGO_network','accepted_currency'])
details['project_name'] = titles
details['vesting_schedule'] = vesting_schedule
details['website'] = website
details['telegram'] = telegram
details['twitter'] = twitter
details['next_claim'] = next_claim
details['swap_percent'] = percent

details =  details[['project_name','symbol','token_price','total_raise','swap_amount','token_network',
                    'IGO_network','accepted_currency','vesting_schedule','next_claim','swap_percent',
                    'website','telegram','twitter']]

details.to_csv('GameFi_ended_launchpad.csv', index=False)

#df = pd.read_csv("GameFi_ended_launchpad.csv")
#new_df = pd.concat([df, details]).drop_duplicates()
#new_df.to_csv("GameFi_launchpad.csv", index=False)