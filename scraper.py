'''
Scrapes current cases, deaths and recoveries with selenium
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd 
from datetime import datetime
import os
from numpy import NaN

#* Setting date and time
now = datetime.now()
date = f"{now.day}/{now.month}/{now.year}"
time_ = f"{now.hour}:{now.minute}"

#* Creating the directory
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "Data", "Scraped Data")
os.makedirs(DATA_DIR, exist_ok=True)
datapath = os.path.join(DATA_DIR, f"Data-{now.date()}.csv")

def scrape_data():
    global date, time_
    #* Running browser without opening browser
    opt = Options()
    opt.add_argument('--headless')

    driver = webdriver.Chrome(options=opt)

    url = "https://www.worldometers.info/coronavirus/"
    driver.get(url)

    #* Getting table data
    time.sleep(2)

    table = driver.find_element_by_id("main_table_countries_today")
    table_body = table.find_element_by_css_selector("tbody")

    table_rows = table_body.find_elements_by_css_selector("tr")

    #* Creating a Data Frame with pandas
    countries = []
    cases = []
    deaths = []
    recoveries = []
    for i in table_rows:
        if i.get_attribute("class") == 'odd' or i.get_attribute("class") == 'even' or i.get_attribute("class") == "total_row_world odd":
            data = i.find_elements_by_css_selector("td")
            countries.append(data[1].text)
            cases.append(data[2].text)
            deaths.append(data[4].text)
            recoveries.append(data[6].text)

    dataframe_dict = {"Countries":countries,
                    "Total Cases":cases,
                    "Total Deaths":deaths,
                    "Total Recoveries":recoveries,
                    "Date":date}

    return dataframe_dict

dataframe = scrape_data()
df = pd.DataFrame(dataframe)
df.fillna("")
df.to_csv(f"{datapath}", index=False)

