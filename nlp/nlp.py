import pandas as pd
import json, codecs, requests, csv

APIKEY = "526a865936msh7e551a58a64b216p195857jsnaf0b6c6d183d"

def analyze(df, rows, entities):
    start = int(rows[-1][0]) + 1
    end = start + 5
    last_text = ""
    for index, entry in df.iterrows():
        if index < start:
            continue
        if index == end:
            break

        title = entry.title.replace("&", " ")
        text = entry.text.replace("&", " ")
        negative = 0
        neutral = 0
        positive = 0
        if last_text != text:
            last_text = text
            document = title + "\n" + text
            sentiment = sentiment_analysis(document)
            e = entities_extraction(document)
        
        if (sentiment == "negative"):
            negative = 1
        elif (sentiment == "neutral"):
            positive = 1
        else:
            neutral = 1
        r=[index, entry.date, entry.c, entry.s, entry.title, entry.text, negative, neutral, positive]
        entities[index] = e
        rows.append(r)

    with open('nlp.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
    f.close()

    with codecs.open('entities.json', 'w', 'utf-8') as fp:            
        fp.write(json.dumps(entities, ensure_ascii=False, indent=4))
    fp.close()
        

def sentiment_analysis(input):
    url = "https://aylien-text.p.rapidapi.com/sentiment"

    querystring = {"text": input,
                   "mode":"tweet"}

    headers = {
        'x-rapidapi-host': "aylien-text.p.rapidapi.com",
        'x-rapidapi-key': APIKEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data["polarity"]

def entities_extraction(input):
    url = "https://aylien-text.p.rapidapi.com/entities"

    querystring = { "text" : input }

    headers = {
        'x-rapidapi-host': "aylien-text.p.rapidapi.com",
        'x-rapidapi-key': APIKEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    try:
        return data["entities"]["keyword"]
    except:
        return []

df = pd.read_csv("reddit.csv", names=["date", "c", "s","title","text"])

with open('nlp.csv', 'r', encoding='utf-8', newline='') as csvfile:
    rows = list(csv.reader(csvfile))
csvfile.close()

with open('entities.json') as jsonfile:
    entities = json.load(jsonfile)
jsonfile.close()

analyze(df, rows, entities)