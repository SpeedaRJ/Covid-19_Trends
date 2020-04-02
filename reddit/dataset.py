import pandas as pd
import requests
import json
import time
import datetime
import twint
import csv
from pytrends.request import TrendReq


# GTRENDS #############################################################################
pytrends = TrendReq(hl='en-US', tz=0)

kw_list = ["COVID-19", "Coronavirus", "SARS-CoV-2"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

over_time = pytrends.interest_over_time()
stats_italy = pytrends.interest_by_region(resolution='Italy', inc_low_vol=True, inc_geo_code=False)
related = pytrends.related_topics()

print(over_time)
#######################################################################################

# TWITTER ##############################################################################
def get_user_location(user):
    g = open("locations.txt", "w", encoding="utf-8")
    g.close()
    d = twint.Config()
    d.Username = user
    d.Format = "{location}"
    d.Hide_output = True
    d.Output = "locations.txt"
    twint.run.Lookup(d)
    g = open("locations.txt", "r", encoding="utf-8")
    return g.readlines()[-1].strip()


def gather_tweets():
    c = twint.Config()
    c.Search = "\"COVID-19\" OR \"Coronavirus\" OR \"SARS-CoV-2\""
    c.Output = "searches.csv"
    c.Stats = True
    # Trenutno bo to limitless search, lahko nastavš število k se zaokrož nauzgor na večkratnik števila 20 al pa datume po katerih hočš iskat
    #c.Limit = 21
    #c.Since = "2020-2-2"
    #c.Until = "2020-3-3"
    c.Hide_output = True
    c.Store_csv = True
    twint.run.Search(c)


def write_data():
    with open("searches.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        n = "\n"
        for row in reader:
            line = f"{get_user_location(row['username'])}|{row['date']}|{row['time']}|" \
                   f"{row['tweet'].replace(n, '')}|{row['hashtags'].replace('[', '').replace(']', '')}|{row['replies_count']}|{row['retweets_count']}" \
                   f"{row['likes_count']}\n"
            main.write(line)


main = open("data.txt", "w", encoding="utf-8")
gather_tweets()
write_data()
main.close()
#######################################################################################