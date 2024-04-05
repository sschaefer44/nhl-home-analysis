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

options = Options()
options.add_argument('disable-infobars')
options.add_argument('--incognito')
options.add_argument("start-maximized")

driver = webdriver.Chrome(service=service, options=options)
URL = 'https://www.nhl.com/stats/teams?aggregate=0&reportType=game&seasonFrom=20212022&seasonTo=20232024&dateFromSeason&gameType=2&page=0&pageSize=100&sort=a_teamFullName'


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

for i in range(0, 78):
    driver.get(URL)
    time.sleep(6)
    html = driver.page_source
    soup = bs(html, features='html.parser')
    rows = soup.find_all('div', class_='rt-tr-group')

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
    URL = re.sub(f'&page={i}', f'&page={i+1}', URL)

driver.quit()
df = pd.DataFrame(zip(team, date, win, loss, ot, points, RW, ROW, SOW, goals, goals_against, power_play, penalty_kill, net_ppp, net_pkp, shots, shots_a, FOWp),
    columns = ['team', 'date', 'win', 'loss', 'ot', 'points', 'RW', 'ROW', 'SOW', 'goals', 'goals_against', 'power_play', 'penalty_kill', 'net_ppp', 'net_pkp', 'shots', 'shots_against', 'FOWp'])

df.to_csv('Regular_Season_Table.csv')