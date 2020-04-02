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
            
    
