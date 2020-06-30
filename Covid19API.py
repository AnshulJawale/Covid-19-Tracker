import requests, os
import pandas as pd

#* https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest
#* https://api.covid19api.com/total/country/{country_slug}

def get_csv(country:str):
    r1 = requests.get("https://api.covid19api.com/countries")
    data1 = r1.json()
    for i in data1:
        if i["Country"] == country or i["Slug"] == country.lower() or i["Slug"] == country.lower().replace(' ', '-'):
            country_slug = i["Slug"]       
            url = f"https://api.covid19api.com/total/country/{country_slug}"

    r = requests.get(url)
    data = r.json()

    countries = []
    cases = []
    deaths = []
    recoveries = []
    dates = []
    for i in data:
        countries.append(i["Country"])
        cases.append(i["Confirmed"])
        deaths.append(i["Deaths"])
        recoveries.append(i["Recovered"])
        dates.append(i["Date"][0:10])

    BASE_DIR = os.path.dirname(__file__)
    COUNTRY_DIR = os.path.join(BASE_DIR, "Data", "Countries")
    os.makedirs(COUNTRY_DIR, exist_ok=True)
    country_path = os.path.join(COUNTRY_DIR, f"{country}.csv")

    country_df = pd.DataFrame({"Country":countries, "Total Cases":cases, "Total Deaths":deaths, "Total Recoveries":recoveries, "Date":dates}, index=list(range(1, len(countries)+1)))

    country_df.to_csv(country_path, index=False)

if __name__ == "__main__":
    country = ""
    try:
        get_csv(country)
        print("Done")
    except:
        print("Try Again")