#Webscraping script to get data from NHL website. 

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
service = Service('/opt/homebrew/bin/chromedriver')
import time
import re
import numpy as np
import pandas as pd
import os 

#Set the chrome options
options = Options()
options.add_argument('disable-infobars')
options.add_argument('--incognito')
options.add_argument("start-maximized")
#Set the driver to my chrome using the selenium web driver library
driver = webdriver.Chrome(service=service, options=options)
#URL to page that will be scraped
URL = 'https://www.nhl.com/stats/teams?aggregate=0&reportType=game&seasonFrom=20212022&seasonTo=20232024&dateFromSeason&gameType=2&page=0&pageSize=100&sort=a_teamFullName'

#Arrays that correspond to each column in the NHL.com table
team = []
date = []
win = []
loss = []
ot = []
points = []
RW = []
ROW = []
SOW = []
goals = []
goals_against = []
power_play = []
penalty_kill = []
net_ppp = []
net_pkp = []
shots = []
shots_a = []
FOWp = []
#Refreshes the page as many times as the for loop says
for i in range(0, 78):
    driver.get(URL)
    #The .sleep ensures all data is loaded on the webpage before the scraping begins.
    time.sleep(6)
    html = driver.page_source
    #BeautifulSoup parses the html
    soup = bs(html, features='html.parser')
    #Looks for rows with the 'rt-tr-group' tag. Tag was identified using Inspect Element
    rows = soup.find_all('div', class_='rt-tr-group')
    #Looks for each 'rt-td' tag in the table group. Adds each item with the 'rt-td' tag to the correct array.
    for row in rows:
        all_data = row.find_all('div', class_='rt-td')

        team.append(all_data[1].text.strip())
        date.append(all_data[2].text.strip())
        win.append(all_data[4].text.strip())
        loss.append(all_data[5].text.strip())
        ot.append(all_data[7].text.strip())
        points.append(all_data[8].text.strip())
        RW.append(all_data[10].text.strip())
        ROW.append(all_data[11].text.strip())
        SOW.append(all_data[12].text.strip())
        goals.append(all_data[13].text.strip())
        goals_against.append(all_data[14].text.strip())
        power_play.append(all_data[17].text.strip())
        penalty_kill.append(all_data[18].text.strip())
        net_ppp.append(all_data[19].text.strip())
        net_pkp.append(all_data[20].text.strip())
        shots.append(all_data[21].text.strip())
        shots_a.append(all_data[22].text.strip())
        FOWp.append(all_data[23].text.strip())
    #Refreshes the page but changes the url to increase the table page it is on so that it will scrape new data.
    URL = re.sub(f'&page={i}', f'&page={i+1}', URL)
    #quit the driver
driver.quit()
#Creates a Pandas dataframe from the arrays of data.
df = pd.DataFrame(zip(team, date, win, loss, ot, points, RW, ROW, SOW, goals, goals_against, power_play, penalty_kill, net_ppp, net_pkp, shots, shots_a, FOWp),
    columns = ['team', 'date', 'win', 'loss', 'ot', 'points', 'RW', 'ROW', 'SOW', 'goals', 'goals_against', 'power_play', 'penalty_kill', 'net_ppp', 'net_pkp', 'shots', 'shots_against', 'FOWp'])
#Converts the dataframe to a CSV
df.to_csv('Regular_Season_Table.csv')
