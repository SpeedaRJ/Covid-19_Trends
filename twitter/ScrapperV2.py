import twint
import datetime


def gather_tweets(since):
    c = twint.Config()
    c.Search = "\"COVID-19\" OR \"Coronavirus\" OR \"SARS-CoV-2\""
    c.Output = "searches.csv"
    c.Stats = True
    c.Since = since.strftime("%Y-%m-%d")
    c.Until = (since + datetime.timedelta(1)).strftime("%Y-%m-%d")
    c.Limit = 6000
    #c.Hide_output = True
    c.Store_csv = True
    twint.run.Search(c)

#Za vsak dan od 1.1 do 16.3 smo kodo pognali ročno, saj je drugače ob prevelikem številu tweetov twint javljal napake
since = datetime.date(2020, 3, 16)
gather_tweets(since)
