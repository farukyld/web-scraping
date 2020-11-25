from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import pandas as pd
from pandas import Series
import time

# Specifying the location of chromedriver
chromedriver = "E:/Desktop/Project/ProjectsWS/chromedriver.exe"

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=option)

# Initializing lists that will be used to store scraped data and used for creating dataframe at the end
home_teams = []
away_teams = []
home_goals_list = []
away_goals_list = []
match_days = []
season = []
FT = []
division = []
tier = []
total_goal = []
goal_diff = []
results = []
HT = []
home_goals_half_list = []
away_goals_half_list = []
half_results = []
weeks = []
fans_list = []
neutral_list = []
home_red_card_list = []
away_red_card_list = []
half_time_goal = []
half_time_goal_diff = []
season_list = []
season_name = []

# Connecting website
driver.get("http://arsiv.mackolik.com/Puan-Durumu")

# Getting seasons list and adding exceptional seasons manually
cboSeason = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cboSeason")))
cboSeason = Select(cboSeason)
options = cboSeason.options

for ind in range(0, len(options)):
    season_list.append(options[ind].get_attribute("value"))
    season_name.append(options[ind].text)

season_list.append("13110")
season_name.append("2011/12")
season_list.append("13111")
season_name.append("2011/12")
season_list = season_list[::-1]
season_name = season_name[::-1]

# Get
for xx, yy in zip(season_list, season_name):
    driver.get(f"http://arsiv.mackolik.com/Standings/Default.aspx?sId={xx}")

    try:
        gg = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Select2")))
        gg = Select(gg)
        options2 = gg.options
        for ix in range(0, len(options2)):
            if options2[ix].get_attribute("value") not in season_list:
                season_list.append(options2[ix].get_attribute("value"))
                season_name.append(yy)
    except:
        pass

    if len(yy.split("/")) == 2:
        seas = str(yy.split("/")[0])
    else:
        seas = str(int(yy.split("/")[0]) - 1)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Fikstür")))
    element.click()

    cboWeek = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cboWeek")))
    cboWeek = Select(cboWeek)
    options = cboWeek.options
    week = 0
    for index in range(0, len(options)):
        cboWeek.select_by_index(index)
        time.sleep(1)
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dvFixtureInner")))
        trs = table.find_elements_by_tag_name("tr")
        week += 1
        for a in trs:
            if "Fikstür" in a.text:
                continue
            else:
                tds = a.find_elements_by_tag_name("td")

                if int(tds[0].text.split("/")[1]) >= 8:
                    match_day = tds[0].text + f"/{seas}"
                else:
                    seas2 = str(int(seas) + 1)
                    match_day = tds[0].text + f"/{seas2}"

                if tds[2].text == "":
                    fans_list.append(1)
                    neutral_list.append(0)
                elif tds[2].text == "S":
                    neutral_list.append(0)
                    fans_list.append(0)
                elif tds[2].text == "T":
                    fans_list.append(1)
                    neutral_list.append(1)
                elif tds[2].text == "TS":
                    fans_list.append(0)
                    neutral_list.append(1)

                home_team = tds[3].text

                if tds[4].find_elements_by_tag_name("img") != []:
                    home_red_card = int(
                        tds[4].find_elements_by_tag_name("img")[0].get_attribute("src").split('-')[1].split('.gif')[0])
                else:
                    home_red_card = 0

                home_goals = int(tds[5].text.split(' - ')[0])
                away_goals = int(tds[5].text.split(' - ')[1])

                if tds[6].find_elements_by_tag_name("img") != []:
                    away_red_card = int(
                        tds[6].find_elements_by_tag_name("img")[0].get_attribute("src").split('-')[1].split('.gif')[0])
                else:
                    away_red_card = 0

                away_team = tds[7].text

                home_half_goals = int(tds[8].text.split(' - ')[0])
                away_half_goals = int(tds[8].text.split(' - ')[1])

                home_teams.append(home_team)
                away_teams.append(away_team)
                home_goals_list.append(home_goals)
                home_goals_half_list.append(home_half_goals)
                away_goals_half_list.append(away_half_goals)
                away_goals_list.append(away_goals)
                match_days.append(match_day)
                season.append(seas)
                FT.append(str(home_goals) + "-" + str(away_goals))
                HT.append(str(home_half_goals) + "-" + str(away_half_goals))
                division.append("T1")
                tier.append(1)
                total_goal.append(int(home_goals) + int(away_goals))
                goal_diff.append(int(home_goals) - int(away_goals))
                half_time_goal.append(int(home_half_goals) + int(away_half_goals))
                half_time_goal_diff.append(int(home_half_goals) - int(away_half_goals))
                weeks.append(week)
                home_red_card_list.append(home_red_card)
                away_red_card_list.append(away_red_card)

                if int(home_goals) > int(away_goals):
                    results.append("H")
                elif int(home_goals) == int(away_goals):
                    results.append("D")
                else:
                    results.append("A")

                if int(home_half_goals) > int(away_half_goals):
                    half_results.append("H")
                elif int(home_half_goals) == int(away_half_goals):
                    half_results.append("D")
                else:
                    half_results.append("A")

driver.quit()

home_teams = Series(home_teams)
away_teams = Series(away_teams)
home_goals_list = Series(home_goals_list)
away_goals_list = Series(away_goals_list)
match_days = Series(match_days)

season = Series(season)
FT = Series(FT)
division = Series(division)
tier = Series(tier)
total_goal = Series(total_goal)
goal_diff = Series(goal_diff)
results = Series(results)

HT = Series(HT)
home_goals_half_list = Series(home_goals_half_list)
away_goals_half_list = Series(away_goals_half_list)
half_results = Series(half_results)

weeks = Series(weeks)
fans_list = Series(fans_list)
neutral_list = Series(neutral_list)
home_red_card_list = Series(home_red_card_list)
away_red_card_list = Series(away_red_card_list)
half_time_goal = Series(half_time_goal)
half_time_goal_diff = Series(half_time_goal_diff)

df = pd.concat([match_days, season, weeks, home_teams, away_teams, FT, home_goals_list, away_goals_list, division, tier,
                total_goal, goal_diff, results, HT, home_goals_half_list, away_goals_half_list, half_time_goal, half_time_goal_diff,
                half_results, fans_list, neutral_list, home_red_card_list, away_red_card_list], axis=1)
df.columns = ["Date", "Season", "Week", "home", "visitor", "FT", "hgoal", "vgoal", "division", "tier", "totgoal",
              "goaldiff", "result", "HT", "hgoal_half", "vgoal_half", "half_totgoal", "half_goaldiff", "result_half",
              "fans", "neutral", "home_red_card", "visitor_red_card"]

df["Date"] = df["Date"].apply(str)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True).dt.date

df.sort_values(by=['Date'], inplace=True, ascending=True)

df.to_excel('tsl_dataset_son.xlsx', index=False)

