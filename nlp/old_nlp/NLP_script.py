# -*- coding: utf-8 -*-
import json, codecs, csv
import pandas as pd
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class Sentiment:
  def __init__(self, score, magnitude):
      self.score = score
      self.magnitude = magnitude

# Instantiates a client
def analyze(df):
    client = language.LanguageServiceClient()
    rows = [["id","date","comment_score","submission_score","title","text","title_sentiment","title_magnitude","text_sentiment","text_magnitude"]]
    entities = dict()
    last_title = ""
    last_text = ""
    for index, row in df.iterrows():
        if index < 10000:
            continue
        title = row.title
        text = row.text
        if last_title != title:
            s1 = analyze_sentiment(title, client)
            e1 = analyze_entities(title, client)
        if last_text != text:
            s2 = analyze_sentiment(text, client)
            e2 = analyze_entities(text, client)

        e1.extend(e2)
        r=[index, row.date, row.c, row.s, title, text, s1.score, s1.magnitude, s2.score, s2.magnitude]
        rows.append(r)
        entities[index] = e1
        #print("TITLE")
        #print(title)
        #print("Score:", s1.score)
        #print("Magnitude:", s1.magnitude)
        #print("")
        #print("TEXT")
        #print(text)
        #print("Score:", s2.score)
        #print("Magnitude:", s2.magnitude)
        #print("Entities:", e1)

    #print(rows)
    #print(json.dumps(entities, ensure_ascii=False))

    



def analyze_sentiment(input, client):
    try:
        document = types.Document(
            content=input,
            type=enums.Document.Type.PLAIN_TEXT)
        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        #sentiment.magnitude
        #sentiment.score
        return sentiment
    except:
        r=Sentiment('-','-')
        return r

def analyze_entities(input, client):
    try: 
        type_ = enums.Document.Type.PLAIN_TEXT

        language = "en"
        document = {"content": input, "type": type_, "language": language}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = enums.EncodingType.UTF8

        response = client.analyze_entities(document, encoding_type=encoding_type)
        # Loop through entitites returned from the API
        entities = []
        for entity in response.entities:
            entities.append(entity.name)
        return entities
    except:
        return []

df = pd.read_csv("reddit.csv", names=["date", "c", "s","title","text"])
analyze(df)