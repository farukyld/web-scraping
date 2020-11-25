from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series,DataFrame

url = 'https://www.statarea.com/predictions'

# Request content from web page
result = requests.get(url)
c = result.content

# Set as Beautiful Soup Object
soup = BeautifulSoup(c, features='html.parser')

# Go to the section of interest
summary = soup.find_all("div", {'class': 'predictions'})[1]

# Find the tables in the HTML
competitions = summary.find_all("div", {'class': 'competition'})

matches = competitions[3].find_all("div", {'class': 'match'})

matches_list = []
names_list = []
for m in competitions:
    matches = m.find_all("div", {'class': 'match'})
    if len(matches) >= 1:
        for i in range(0, len(matches)):
            matches_list.append(matches[i].find_all("div", {'class': 'value'}))
            names_list.append(matches[i].find_all("div", {'class': 'name'}))

pred = []
home_win = []
draw = []
away_win = []
ht_home_win = []
ht_draw = []
ht_away_win = []
over_1_5 = []
over_2_5 = []
over_3_5 = []
bts = []
ots = []
match_name = []

for k in range(0, len(matches_list)):
    pred.append(matches_list[k][2].text)
    home_win.append(matches_list[k][3].text)
    draw.append(matches_list[k][4].text)
    away_win.append(matches_list[k][5].text)
    ht_home_win.append(matches_list[k][6].text)
    ht_draw.append(matches_list[k][7].text)
    ht_away_win.append(matches_list[k][8].text)
    over_1_5.append(matches_list[k][9].text)
    over_2_5.append(matches_list[k][10].text)
    over_3_5.append(matches_list[k][11].text)
    bts.append(matches_list[k][12].text)
    ots.append(matches_list[k][13].text)
    match_name.append(names_list[k][0].text + " - " + names_list[k][1].text)

pred = Series(pred)
home_win = Series(home_win)
draw = Series(draw)
away_win = Series(away_win)
ht_home_win = Series(ht_home_win)
ht_draw = Series(ht_draw)
ht_away_win = Series(ht_away_win)
over_1_5 = Series(over_1_5)
over_2_5 = Series(over_2_5)
over_3_5 = Series(over_3_5)
bts = Series(bts)
ots = Series(ots)
match_name = Series(match_name)

matches_df = pd.concat([match_name, pred, home_win, draw, away_win, ht_home_win, ht_draw,
                        ht_away_win, over_1_5, over_2_5, over_3_5, bts, ots], axis=1)
matches_df.columns = ['Match Name', 'Prediction', 'Home Win', 'Draw', 'Away Win', 'HT Home Win', 'HT Draw',
                      'HT Away Win', 'Over 1.5', 'Over 2.5', 'Over 3.5', 'BTS', 'OTS']

print(matches_df)
