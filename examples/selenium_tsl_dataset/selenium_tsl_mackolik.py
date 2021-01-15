from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import pandas as pd
import time

# Specifying the location of chromedriver
chromedriver = "E:/Desktop/Project/ProjectsWS/chromedriver.exe"

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# Create new Instance of Chrome in incognito mode
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=option)

# Initializing lists that will be used to store scraped data and used for creating dataframe at the end
df = pd.DataFrame(columns=["Date", "Season", "Week", "home", "visitor", "FT", "h_goal", "v_goal", "division", "tier",
                           "tot_goal", "goal_diff", "result", "HT", "h_goal_half", "v_goal_half", "half_tot_goal",
                           "half_goal_diff", "result_half", "fans", "neutral", "home_red_card", "visitor_red_card"])

season_list = []
season_name = []

# Connecting website
driver.get("http://arsiv.mackolik.com/Puan-Durumu")

# Getting seasons list and adding exceptional seasons manually
cboSeason = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "cboSeason")))
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
        gg = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "Select2")))
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
    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, "Fikstür")))
    element.click()

    cboWeek = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "cboWeek")))
    cboWeek = Select(cboWeek)
    options = cboWeek.options
    week = 0
    for index in range(0, len(options)):
        cboWeek.select_by_index(index)
        time.sleep(1.5)
        table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dvFixtureInner")))
        trs = table.find_elements_by_tag_name("tr")
        week += 1
        for a in trs:
            if "Fikstür" in a.text:
                continue
            else:
                tds = a.find_elements_by_tag_name("td")

                if 'v' in tds[5].text:
                    continue
                elif '-' in tds[5].text:
                    if int(tds[0].text.split("/")[1]) >= 8:
                        match_day = tds[0].text + f"/{seas}"
                    else:
                        seas2 = str(int(seas) + 1)
                        match_day = tds[0].text + f"/{seas2}"

                    if tds[2].text == "":
                        fans = 1
                        neutral = 0
                    elif tds[2].text == "S":
                        neutral = 0
                        fans = 0
                    elif tds[2].text == "T":
                        fans = 1
                        neutral = 1
                    elif tds[2].text == "TS":
                        fans = 0
                        neutral = 1

                    home_team = tds[3].text

                    if tds[4].find_elements_by_tag_name("img"):
                        home_red_card = int(
                            tds[4].find_elements_by_tag_name("img")[0].get_attribute("src").split('-')[1].split('.gif')[0])
                    else:
                        home_red_card = 0

                    home_goals = int(tds[5].text.split(' - ')[0])
                    away_goals = int(tds[5].text.split(' - ')[1])

                    if tds[6].find_elements_by_tag_name("img"):
                        away_red_card = int(
                            tds[6].find_elements_by_tag_name("img")[0].get_attribute("src").split('-')[1].split('.gif')[0])
                    else:
                        away_red_card = 0

                    away_team = tds[7].text

                    home_half_goals = int(tds[8].text.split(' - ')[0])
                    away_half_goals = int(tds[8].text.split(' - ')[1])

                    if int(home_goals) > int(away_goals):
                        result = "H"
                    elif int(home_goals) == int(away_goals):
                        result = "D"
                    else:
                        result = "A"

                    if int(home_half_goals) > int(away_half_goals):
                        half_result = "H"
                    elif int(home_half_goals) == int(away_half_goals):
                        half_result = "D"
                    else:
                        half_result = "A"

                    new_row = {'Date': match_day, "Season": seas, "Week": week, "home": home_team, "visitor": away_team,
                               "FT": str(home_goals) + "-" + str(away_goals), "h_goal": home_goals, "v_goal": away_goals,
                               "division": "T1", "tier": 1, "tot_goal": int(home_goals) + int(away_goals),
                               "goal_diff": int(home_goals) - int(away_goals), "result": result,
                               "HT": str(home_half_goals) + "-" + str(away_half_goals), "h_goal_half": home_half_goals,
                               "v_goal_half": away_half_goals, "half_tot_goal": int(home_half_goals) + int(away_half_goals),
                               "half_goal_diff": int(home_half_goals) - int(away_half_goals), "result_half": half_result,
                               "fans": fans, "neutral": neutral, "home_red_card": home_red_card,
                               "visitor_red_card": away_red_card}

                    df = df.append(new_row, ignore_index=True)

driver.quit()

df["Date"] = df["Date"].apply(str)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True).dt.date

df.sort_values(by=['Date'], inplace=True, ascending=True)

df.to_excel('tsl_dataset_son.xlsx', index=False)

