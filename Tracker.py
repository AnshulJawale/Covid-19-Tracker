import pandas as pd 
import os 
from Covid19API import get_csv
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import numpy as np 

#? Creating csv file if doesnt exist
country = "United States of America"
get_csv(country)

BASE_DIR = os.path.dirname(__file__)
COUNTRY_DIR = os.path.join(BASE_DIR, "Data", "Countries")
country_path = os.path.join(COUNTRY_DIR, f"{country}.csv")
country_df = pd.read_csv(country_path)

country_df["Date"] = pd.to_datetime(country_df["Date"])                 #? Converting string to date

#* Creating new cases, deaths, recoveries per day columns
country_df["New Cases"] = country_df['Total Cases'] - country_df['Total Cases'].shift(1)
country_df["New Deaths"] = country_df['Total Deaths'] - country_df['Total Deaths'].shift(1)
country_df["New Recoveries"] = country_df['Total Recoveries'] - country_df["Total Recoveries"].shift(1)

imputer = SimpleImputer(strategy='constant')

#? Arranging according to date
country_df = country_df.groupby(["Date"])["Country", "Total Cases", "New Cases" , "Total Deaths", "New Deaths","Total Recoveries", "New Recoveries", "Date"].sum().reset_index()

def rate_of_change():
    plt.plot(country_df["Date"], country_df["New Cases"], label="New Cases")
    plt.plot(country_df["Date"], country_df["New Deaths"], label="New Deaths")
    plt.plot(country_df["Date"], country_df["New Recoveries"], label="New Recoveries")
    plt.title(label=f"{country}-Reports per day")
    plt.xlabel("Date")
    plt.ylabel("Reports")
    plt.legend()
    plt.show()

def total():
    plt.plot(country_df["Date"], country_df["Total Cases"], label="Total Cases")
    plt.plot(country_df["Date"], country_df["Total Deaths"], label="Total Deaths")
    plt.plot(country_df["Date"], country_df["Total Recoveries"], label="Total Recoveries")
    plt.title(label=f"{country}-Total Reports")
    plt.xlabel("Date")
    plt.ylabel("Reports")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    print(country_df)
    rate_of_change()
    total()    