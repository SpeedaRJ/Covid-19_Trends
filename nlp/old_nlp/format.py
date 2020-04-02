import csv
import pandas as pd

df = pd.read_csv("nlp.csv", names=["index", "date", "c", "s", "title", "text", "title_sentiment", "nvm1", "text_sentiment", "nvm2"])
rows = [["id","date","comment_score","submission_score","title","text","negative","neutral","positive"]]
for index, entry in df.iterrows():
    if index == 0:
        continue
    if(entry.text_sentiment == "-"):
        negative = -9999
        neutral = -9999
        positive = -9999
    else:
        sentiment = float(entry.text_sentiment)
        negative = 0
        neutral = 0
        positive = 0
        if(sentiment <= -1/3):
            negative = 1
        elif(sentiment < 1/3):
            neutral = 1
        else:
            positive = 1
    r=[entry['index'], entry.date, entry.c, entry.s, entry.title, entry.text.replace("&", " "), negative, neutral, positive]
    rows.append(r)

df = pd.read_csv("nlp2.csv", names=["index", "date", "c", "s", "title", "text", "title_sentiment", "nvm1", "text_sentiment", "nvm2"])
for index, entry in df.iterrows():
    if index == 0:
        continue
    if(entry.text_sentiment == "-"):
        negative = -9999
        neutral = -9999
        positive = -9999
    else:
        sentiment = float(entry.text_sentiment)
        negative = 0
        neutral = 0
        positive = 0
        if(sentiment <= -1/3):
            negative = 1
        elif(sentiment < 1/3):
            neutral = 1
        else:
            positive = 1
    r=[entry['index'], entry.date, entry.c, entry.s, entry.title, entry.text.replace("&", " "), negative, neutral, positive]
    rows.append(r)

df = pd.read_csv("nlp3.csv", names=["index", "date", "c", "s", "title", "text", "title_sentiment", "nvm1", "text_sentiment", "nvm2"])
for index, entry in df.iterrows():
    if index == 0:
        continue
    if(entry.text_sentiment == "-"):
        negative = -9999
        neutral = -9999
        positive = -9999
    else:
        sentiment = float(entry.text_sentiment)
        negative = 0
        neutral = 0
        positive = 0
        if(sentiment <= -1/3):
            negative = 1
        elif(sentiment < 1/3):
            neutral = 1
        else:
            positive = 1
    r=[index, entry.date, entry.c, entry.s, entry.title, entry.text.replace("&", " "), negative, neutral, positive]
    rows.append(r)

with open('natural_language.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)