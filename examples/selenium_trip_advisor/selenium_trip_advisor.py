from selenium import webdriver
import time


def remove_items_from_list(ordered_list, temp):
    n = len(ordered_list)
    for i in range(n - 1, -1, -1):
        if ordered_list[i] in temp:
            del ordered_list[i]


chromedriver = "__PATH__/chromedriver.exe"

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--start-maximized")

# Create new Instance of Chrome in incognito mode
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=option)

driver.get(
    "https://www.tripadvisor.co.uk/Restaurant_Review-g186338-d5122082-Reviews-Alexander_The_Great-London_England.html#REVIEWS")

time.sleep(3)
cookie_button = driver.find_element_by_id(
            "_evidon-accept-button")
cookie_button.click()

page_numbers = driver.find_elements_by_xpath("//div[@class='pageNumbers']")

if "…" not in page_numbers[0].text:
    max_page_number = int(page_numbers[0].text[-1])
else:
    max_page_number = int(page_numbers[0].text.split("…")[-1])

time.sleep(1)

review_titles_list = []
reviews_list = []
managerReply_list = []

for x in range(max_page_number):

    if x != 0:
        time.sleep(2)
        next_page_button = driver.find_elements_by_xpath(
            "//a[@class='nav next ui_button primary']")
        next_page_button[0].click()
        time.sleep(1)

    elements = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")

    for element in elements:
        try:
            element.click()
            time.sleep(1)
        except:
            pass

    review_titles = driver.find_elements_by_xpath("//div[@class='quote']")

    reviews = driver.find_elements_by_xpath("//p[@class='partial_entry']")

    managerReply = driver.find_elements_by_xpath(
        "//div[contains(@class,'mgrRspnInline')]//p[contains(@class,'partial_entry')]")

    remove_items_from_list(reviews, managerReply)

    for x in range(0, len(review_titles)):
        review_titles_list.append(review_titles[x].text)
        reviews_list.append(reviews[x].text)

    for y in managerReply:
        managerReply_list.append(y.text)
