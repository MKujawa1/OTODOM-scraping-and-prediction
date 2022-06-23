from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

### Get random user agent 
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agents = user_agent_rotator.get_user_agents()

### Get user agent
all_data = pd.DataFrame({'cost':[],'meters': [],'rooms': [],'dist': []})
### Start scraping
pages = 101
for page in range(1,pages):
    ### Get random time and user agent
    time.sleep(random.uniform(0.1, 0.6))
    user_agent = user_agent_rotator.get_random_user_agent()
    ### Get URL and request
    URL = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/poznan?distanceRadius=0&page={page}&limit=36&market=PRIMARY&priceMax=700000&ownerTypeSingleSelect=ALL&locations=%5Bcities_6-1%5D&viewType=listing'
    data = requests.get(URL,{'User-Agent':user_agent})
    ### Data parse
    cont = BeautifulSoup(data.content, 'html.parser')
    ### Init list to append data
    room =[]
    meter = []
    cost = []
    dist = []
    floors = []
    ### Get all data about flats
    apart = cont.find_all('li',class_ = 'css-p74l73 es62z2j17')
    ### Start from 3. Previous datas are promoted
    for i in range(3,len(apart)):
        ### Get main data about flat
        ap_info = apart[i].find('article',class_ = 'css-1th7s4x es62z2j16')
        r = int(ap_info.find_all('span')[3].get_text().split(' ')[0])
        m = float(ap_info.find_all('span')[4].get_text().split(' ')[0])
        c = ap_info.find_all('span')[1].get_text()
        d = ap_info.find_all('span')[0].get_text().split(',')[1][1:]
        ### If threre is no price
        if c == 'Zapytaj o cenę':
            pass
        else:
            ### Get data about floor
            time.sleep(random.uniform(0.1, 0.4))
            full_link = 'https://www.otodom.pl'+apart[i].find('a')['href']
            floor = requests.get(full_link,{'User-Agent':user_agent})
            floor = BeautifulSoup(floor.content,'html.parser')
            floor = floor.find('div', class_ = 'css-wj4wb2 emxfhao1')
            floor = floor.find_all('div',class_='css-1ccovha estckra9')
            bool_data = [i['aria-label']=='Piętro' for i in floor]
            floor_data = floor[np.argmax(bool_data)].find('div', class_='css-1wi2w6s estckra5').get_text().split('/')[0]
            if floor_data == 'parter':
                ### Convert floor to 0
                floor_data = 0
                ### Convert cost data to int
                c = int(c.replace('zł','').replace('\xa0','').replace(',','.'))
                ### Append data
                room.append(r)
                meter.append(m)
                cost.append(c)
                dist.append(d)
                floors.append(floor_data)
            else:
                try:
                    ### Convert floor to int
                    floor_data = int(floor_data)
                    ### Convert cost data to int
                    c = int(c.replace('zł','').replace('\xa0','').replace(',','.'))
                    ### Append data
                    room.append(r)
                    meter.append(m)
                    cost.append(c)
                    dist.append(d)
                    floors.append(floor_data)
                except:
                    pass
    ### Append data to DataFrame
    all_data = all_data.append(pd.DataFrame({'cost':cost,'meters': meter,'rooms': room,'dist': dist,'floor':floors}),ignore_index = True)
    ### Print current page
    print(page)
### Save data to csv
all_data.to_csv(r'D:\GIT_PYTHON\OTODOM-scraping-and-prediction\otodom_data.csv',sep=',')
