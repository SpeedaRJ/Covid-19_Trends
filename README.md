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
