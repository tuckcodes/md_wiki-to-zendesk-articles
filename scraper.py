import time
import csv
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


#________________________________________________________________
# ONLY EDIT THESE SETTINGS!!!!!!!!!!!!!!!!!!!!



#zendesk articles section that you want to upload to
# You can use curl to GET https://rancherfederal.zendesk.com/api/v2/help_center/en_us/sections   <<<<<----
section_url = "https://rancherfederal.zendesk.com/api/v2/help_center/sections/{section_id}"
credentials = 'your_zendesk_email', 'your_zendesk_password'
zendesk = 'https://rancherfederal.zendesk.com'




# END EDIT AREA. DO NOT CHANGE SETTINGS AFTER THIS LINE!!!!!
#________________________________________________________________


# Use default chrome profile
service = Service("./driver/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
options.add_argument("user-data-dir=C:\\Users\\primary\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
options.add_argument("--headless")
options.add_argument("--window-size=1280,800");
options.add_argument("--allow-insecure-localhost")

# Chrome driver
browser = webdriver.Chrome(service=service, options=options)

# start message
print("loading data...")

# Where to scrape
wiki = 'https://wiki.rfed.dev'
browser.get(wiki)

# What to scrape for
time.sleep(.1)
browser.find_element(By.XPATH, '//*[@id="app"]/div/nav/div[1]/div/div/div/div[1]/div/div[2]').click() #click knowledgebase
time.sleep(.1)
browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/nav/div[1]/div/div/div/div[1]/div/div[4]').click() #click engineering guides

time.sleep(1)

fieldnames = ['section_id', 'title', 'body', 'author_id', 'source_locale', 'permission_group_id', 'user_segment_id']
articles = {}
elms = browser.find_elements(By.XPATH, '//a[contains(@href, "EG-")]') # find elms by relevant href
urls = []
count = 1

for elm in elms:
    url = elm.get_attribute("href") # get url
    urls.append(url)

# Create list for github csv import
for url in urls:
    article={}
    total=len(urls)
    
    # create title
    title = url.removeprefix('https://wiki.rfed.dev/en/Knowledge-Base/Engineering-Guides/EG-') # get title from url
    title = title.replace('-', ' ') # clean up title
    
    # get body
    browser.get(url) # use the url from the current iteration
    time.sleep(.1)
    body = browser.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div/div[2]/div[2]/div').get_attribute('innerHTML') # get the html
    time.sleep(.1)
           
    # add zendesk article attributes to dict
    article["body"] = body
    article["locale"] = "en-us"
    article["title"] = title
    article["source_locale"] = "Tucker Blue"
    article["permission_group_id"] = "Tucker Blue"
    article["user_segment_id"] = "Tucker Blue"

    articles["article"] = article # add dict to to articles list as a 'article' line item
    
    # progress counter
    print(count,"/",total)
    count=count+1

# UNCOMMENT THIS SECTION FOR TESTING
    
    if count == 3:

        json_object = json.dumps(articles, indent = 4) 
        print(json_object)

# END TESTING SECTION        
        
# dont notify all users that new articles have been created. Warning, turning to true could cause spam.
articles["notify_subscribers"] = "false"   

# # api call to POST new articles
#upload = requests.post(url=section_url, data=articles)
# upload.auth = credentials
# upload 

print("Exported", len(articles), "articles to csv for Github consumption!")