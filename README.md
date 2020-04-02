# COVID-19 and Social Media

Epidemija COVID-19 se v trenutnem ćasu razširja na pandemijo, ljudje so v samoizolaciji, nekateri trpijo kot direktna posledica, nekateri pa indirektno. Projekt smo pričeli z kreiranjem podatkovne mnozice, katero smo pretransformirali v uporabno obliko, poleg tega, pa smo tudi uporabili nekatere podatkovne mnozice na Kaggle za natanćne statistike širjenja števila okužb, ozdravelih in mrtvih posameznikov.

Zadnjih nekaj tednov smo se sestali preko raznih medijev in skongruirali 3 razlićne vire v 3 lastne podatkovne množice ter nato iz njih naredili še tri bolj uporabne, katere so posledica uporabe metod naravnega procesiranja jezika nad prvotnimi množicami.

Radi bi razdelili napredek na tri glavne faze, vsaka od njih je vzela doloćen ćas, već podrobnosti pa v nadaljnih sekcijah.

## 1. faza: Webscrape API za socialne medije
Po doloćenih ovirah smo se odloćili za Twitter, Reddit ter GTrends, saj so se nam zdeli najbolj zanimivi. Moramo izpostaviti, da taki API-ji, ki ponujajo moznost pridobivanja tekstovne vsebine objav so precej omejeni s klici, poleg tega, smo pa morali to prilagoditi ćasovnem intervalu za nekaj mesecov nazaj, zato je ta faza bila tudi najdaljša.

### Reddit - https://pushshift.io/
Redditov lastni API, ki ponuja poleg agregiranih statistik, tudi moznost pridobivanja vsebin tako-imenovanih 'submission'-ov ter komentarjev. Podatki so skonstruirani na naslednji naćin:

Datum, Ocena Komentarja, Ocena Submmissiona, Naslov Submissiona, Text Komentarja

Po zgornjem formatu imamo trenutno podatke od 16. marca do 27. januarja tega leta. 
Naslednji odsek kode je bil uporabljen za zgradbo te množice, veliko je olajšal delo modul psaw:
```Python
from psaw import PushshiftAPI
import datetime as dt
import csv
api = PushshiftAPI()
start_epoch=int(dt.datetime(2020, 1, 1, 0, 0, 0).timestamp())
before = int(dt.datetime(2020, 1, 21, 2, 0, 0).timestamp())


cache = 0
f =  open(r'reddit21.csv', 'w')
writer = csv.writer(f)
while( before>start_epoch ):
    gen = api.search_comments(after=start_epoch, before=before,  subreddit="Coronavirus")
    for c in gen:
        print(cache)
        print(dt.datetime.fromtimestamp( c.created_utc ))
        submission = list(api.search_submissions(ids = [c.link_id.split("_")[1]]))
        if(len(submission)>0):
            submission = submission[0]
        else:
            continue
        writer.writerow([ dt.datetime.fromtimestamp( c.created_utc ).date(), c.score, submission.score, (submission.title).replace("\n"," ") , (c.body).replace("\n"," ") ])
        #before = c.created_utc 
        cache += 1   
        if( cache%105==0 ):
            before -= 60 * 60
            gen = api.search_comments(after=start_epoch, before=before,  subreddit="Coronavirus")
```








# Hitra analiza podatkov o Tweetih iz strani Kaggle

Medtem ko se pripravlja naša baza z Tweeti od 1.1.2020 do 16.3.2020, ki vsebuje vzorec šest tisočih Tweetov iz vsakega dneva, ki omenjajo Koronavirus. Za sprotno poročilo smo se odločili da naredimo hitro analizo na tovrstnih podatkih iz Kaggla, ki jih nato lahko uporabimo za primerjavo kasneje z našimi podatki. V ta namen smo Kagglovo bazo pretvorili v format, ki smo ga izbrali tudi mi za našo bazo: Datum - Lokacija - Tweet - Število všečkov - Število retweetov. Odločili smo se, da nad temi podatki naredimo hitro analizo, tako da imamo neko primerjavo z našimi podatki, kot da dobimo in se seznanimo z vrsto podatkov. Kaggle baza je sicer zgolj za marec, od prvega do dvaindvajsetega, vzeli smo pa prav tako vzorec prvih 6000 Tweetov iz vsake csv datoteke, kjer smo za prvo izbrali 6000 za vsak dan in dobili 114000 tweetov velik vzorec.

Za potrebe vmesnega poročila smo uporabili naslednje knjižnice:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import scipy.stats as sc
```

Vseh 12 csv datotek smo prebrali in pretvorili v en sam pandas DataFrame.
```python
tweets1 = pd.read_csv("./Kaggle/2020-03-00 Coronavirus Tweets (pre 2020-03-12).CSV")
tweets2 = pd.read_csv("./Kaggle/2020-03-12 Coronavirus Tweets.CSV")
tweets3 = pd.read_csv("./Kaggle/2020-03-13 Coronavirus Tweets.CSV")
tweets4 = pd.read_csv("./Kaggle/2020-03-14 Coronavirus Tweets.CSV")
tweets5 = pd.read_csv("./Kaggle/2020-03-15 Coronavirus Tweets.CSV")
tweets6 = pd.read_csv("./Kaggle/2020-03-16 Coronavirus Tweets.CSV")
tweets7 = pd.read_csv("./Kaggle/2020-03-17 Coronavirus Tweets.CSV")
tweets8 = pd.read_csv("./Kaggle/2020-03-18 Coronavirus Tweets.CSV")
tweets9 = pd.read_csv("./Kaggle/2020-03-19 Coronavirus Tweets.CSV")
tweets10 = pd.read_csv("./Kaggle/2020-03-20 Coronavirus Tweets.CSV")
tweets11 = pd.read_csv("./Kaggle/2020-03-21 Coronavirus Tweets.CSV")
tweets12 = pd.read_csv("./Kaggle/2020-03-22 Coronavirus Tweets.CSV")

tweets = tweets1.append(tweets2.head(6000)).append(tweets3.head(6000)).append(tweets4.head(6000))
tweets = tweets.append(tweets5.head(6000)).append(tweets6.head(6000)).append(tweets7.head(6000)).append(tweets8.head(6000))
tweets = tweets.append(tweets9.head(6000)).append(tweets10.head(6000)).append(tweets11.head(6000)).append(tweets12.head(6000))
tweets = tweets.rename(columns={"status_id": "status_id","created_at": "Date", "text": "Tweet", "favourites_count": "Likes", "retweet_count": "Retweets", "country_code": "Location"})
tweets["Date"] = [dt.datetime.strptime(tweets["Date"].values[i].split("T")[0], "%Y-%m-%d") for i in range(len(tweets))]
tweets = tweets.groupby("Date").head(6000)
```

### Pregled osnovnih statističnih podatkov

Najbolj osnovna statistika, ki jo lahko pregledamo je povprečno število všečkov in retweetov na tweet, ter povprečni standardni odklon le teh.
```python
likes_mean = tweets["Likes"].mean()
likes_std = tweets["Likes"].std()
retweets_mean = tweets["Retweets"].mean()
retweets_std = tweets["Retweets"].std()
```
Dobimo rezultate da je povprečje všečkov na tweet 15391.429 s standardnim odklonom 43243.936, za retweet-e pa dobimo rezultate da je povprečnje na tweet 5.115 s standardnim odklonom 138.549. Iz tega vidimo da je pri obeh velik standardni odklon. Seveda je to tudi nekako pričakovano saj imajo različni računi različno število sledilcev in posledično različno "prometa", ki gre čez njihov račun. Lahko razberemo, da je takih, ki imajo manj sledilcev veliko več kot pa teh z velikim številom le teh. Takih podatkov kot je število sledilcev, ali je račun potrjen itd. v naši bazi ne bomo imeli, je pa zanimivo razmisliti kako vplivajo na podatke.

Podatke lahko predstavimo kot da gre za normalno porazdelitev. Če to storimo lahko bodimo nasledne grafe.
```python
(mean, std) = sc.norm.fit(list(tweets["Likes"]))
plt.figure(figsize=(8,8))
top_quantile = sc.norm.ppf(0.75, mean, std)
plt.subplot(1,3,1)
plt.hist(tweets[tweets["Likes"] < top_quantile]["Likes"], edgecolor="black")
bottom_half = sc.norm.ppf(0.50, mean, std)
plt.subplot(1,3,2)
plt.hist(tweets[tweets["Likes"] < bottom_half]["Likes"], color="Orange", edgecolor="black")
bottom_qunatile = sc.norm.ppf(0.40, mean, std)
plt.subplot(1,3,3)
plt.hist(tweets[tweets["Likes"] < bottom_qunatile]["Likes"], color="Green", edgecolor="black")
```
![3graphs.png](attachment:3graphs.png)
Vidimo da število tweetov glede na število všečkov, praktično logaritmično pada z večjim število všečkov. To je uvidno tako v tweetih, ki imajo okoli 4000 všečkovi in manj (zeleni graf) kot na tistih, ki imajo okoli 40000 všečkov in manj (modri graf). Pri vseh treh percentilih za katere smo naredili graf po normalni porazdelitvi, torej 75-percentil, 50-percentil in 40-percentil, se opazi enak vzorec padanja števila tweetov z večjih številom všečkov. 

Zanima nas tudi število všečkov in retweetov glede na posamezni dan, tako lahko nekako vidimo kako je potek "promet".
```python
plt.figure(figsize=(8,10))
sum_likes = tweets.groupby("Date").sum()
sum_retweets = tweets.groupby("Date").sum()
plt.subplot(2,1,1)
sum_likes["Likes"].plot.barh(color="cyan", edgecolor="black")
plt.subplot(2,1,2)
sum_retweets["Retweets"].plot.barh(color="olive", edgecolor="black")
```
![promet.png](attachment:promet.png)
Če "promet" po določenem dnevu opredelimo kot seštevek všečkov in retweetov, vidimo da je bilo največ prometa okoli desetega ali pa enajstega marca. Ker bodo te dnevi prisotni tudi v naši bazi, bomo lahko na podlagi tega naredili primerjave med načinon zajemanja podatkov, ki smo ga uporabili mi, in tem, ki so ga uporabili za Kaggle baze.

Ker bomo v naših podatkih pregledovali tudi tweete glede na lokacije, nas zanima, kako so loakcije razporejene v Kaggle bazah. Kar nam vrne spodnji graf.
```python
locations = tweets[tweets["Location"].notnull()]
locations_count = locations.groupby("Location").count()
locastions_count[locastions_count["user_id"] > 30]["user_id"].sort_values().plot.barh(color="wheat", edgecolor="black")
```
![locations.png](attachment:locations.png)
Iz vseh 114000 tweetov, ki smo jih vzeli za vzorec, jih je le 5976 imelo navedeno lokacijo. Izmed teh 5976 tweetov dobimo 111 različnih držav. Te smo za potrebe grafa omejili na tiste, ki so imeli več kot 30 tweetov v obdobju od prvega do dvaindvajsetega marca. Izkaže se da je takih le 24. Izmed teh 24 se vidi da Amerika množično prevladuje, sledita ji še Kanda in Velika Britanija, torej še dve angleško govoreči državi, ampak Ameriki nista blizu. To je podatek, ki ga bomo tudi mi lahko spremljaji v naši bazi, in ga primerjali s podatki, ki smo jih dobili iz Kaggle-ove baze. 

Za zaključek, lahko te podatke še simplistično pregledamo na podlagi vsebine samega tweeta. Zanima nas naprimer koliko ljudje govorijo o obolelih, o novih primerih, o smrtih in ozdravelih. Iz teh podatkov dobimo nasledni graf. 
```python
recovered = len(tweets[tweets["Tweet"].str.contains("recover.*")])
ill = len(tweets[tweets["Tweet"].str.contains("infected.*")])
new = len(tweets[tweets["Tweet"].str.contains("new case.*")])
dead = len(tweets[tweets["Tweet"].str.contains("dead")])
death = len(tweets[tweets["Tweet"].str.contains("death")])
healthy = len(tweets[tweets["Tweet"].str.contains("health.*")])
plt.bar(["Recovered", "Ill", "New", "Dead", "Death", "Healthy"],[healthy, recovered, new, ill, death, dead], color="maroon", edgecolor="black")
```
![words.png](attachment:words.png)
Iz njega lahko vidimo da jih največ (po našem zelo omejenem iskanju) govori o teh, ki so ozdraveli, temu pa sledijo tweeti, ki vsebujejo besedo death. Z hitrim pogledom v podatke vidimo, da gre pri teh tweetih dejansko za avtomatiziran profil, ki objavlja statusne spremembe.

# Priprava naše podatkovne baze

Našo podatkovno bazo bomo pripravili z pomočjo twitter scrapperja in ne direktno z uporabo Twitter API. Uporabili bomo twint, GitHub modul, ki je namenjen javni uporabi. Ima opcijo iskanja tako po besedah kot po uporabnikih. Koda za samo proces pridobivanja podatkov je bila sledeča:
```python
import twint

c = twint.Config()
c.Search = "\"COVID-19\" OR \"Coronavirus\" OR \"SARS-CoV-2\""
c.Output = "searches.csv"
c.Stats = True
c.Since = since.strftime("2020-01-01")
c.Until = (since + datetime.timedelta(1)).strftime("2020-01-02")
c.Limit = 6000
#c.Hide_output = True
c.Store_csv = True
twint.run.Search(c)
```
Kodo smo pognali za vsak dan posebaj do 15.3.2020, tako da smo dobili vzorec 6000 tweetov dnevno. To pa za potrebe naše analize ni zadostovalo saj ne vsebuje lokacije. Na srečo nam pa twint omogoča pogledati lokacijo uporabnika, ki je objavil tweet. 
```python
g = open("locations.txt", "w", encoding="utf-8")
g.close()
d = twint.Config()
d.Username = user
d.Format = "{location}"
d.Output = "locations.txt"
twint.run.Lookup(d)
```
Ko smo enkrat imeli vse tweete za našo bazo smo morali dati vse še čez program, ki je za vsak tweet pogledal njegovo lokacijo. To smo zapisali v txt datoteko, nato pa iz nje prebrali to vrednost in jo shraili v csv, katerega bomo kasneje uporabili za analizo vseh podatkov. Ker je nekaj uporabnikov, ki imajo za lokacijo podano nekaj kar ni realna geografska lokacija, bomo ob končanem preračunavanju lokacij, morali še pregledati katere lokacije so pravilne. To lahko storimo z python modulom GeoPy, ki nam ne bo vrnil vrednosti, če lokacija ne bo pravilna. S pomočjo tega bomo nato lahko izvedli analizo nad podatki glede na države.
