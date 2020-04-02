import twint
import datetime
import csv
import geopy.geocoders as gg


#Odsek kode ki bo kasneje uporabljen za preverjanje lokacij
def get_country_code(location):
    try:
        locator = gg.Nominatim(user_agent="myGeocoder")
        location = locator.geocode(location, addressdetails=True)
        print(location.raw["address"]["country_code"].upper())
        return location.raw["address"]["country_code"].upper()
    except:
        print("")
        return ""

#Iskanje uporabnikove lokacije
def get_user_location(user, i):
    g = open("locations.txt", "w", encoding="utf-8")
    g.close()
    d = twint.Config()
    d.Username = user
    d.Format = "{location}"
    d.Output = "locations.txt"
    twint.run.Lookup(d)
    g = open("locations.txt", "r", encoding="utf-8")
    return "".join(g.readlines()).strip()

#Ker so podatki z eno uro zamika, to preoblikujemo da imamo dejansko pravilne datume
#Ko smo scrappali za 15.3 je začelo ob 16.3 ob prvi uri zjutraj in šlo nazaj
def transform_date(date, time):
    date_x = date.split("-")
    time_x = time.split(":")
    date_out = datetime.datetime(int(date_x[0]), int(date_x[1]), int(date_x[2]), int(time_x[0]), int(time_x[1]), int(time_x[2]))
    date_out -= datetime.timedelta(hours=1)
    return date_out.date()

#Branje tweetov in zapis v uporabno tabelo
def write_data():
    with open("searches.csv", newline='', encoding="utf-8") as csvfile:
        with open('TwitterData.csv', 'w', newline='', encoding="utf-8") as csvfileW:
            fieldnames = ["Date", "Location", "Tweet", "Hashtags", "Retweets", "Likes"]
            writer = csv.DictWriter(csvfileW, fieldnames)
            writer.writeheader()
            reader = csv.DictReader(csvfile)
            n = "\n"
            i = 0
            for row in reader:
                i += 1
                print(i)
                tweet = row["tweet"].replace(n, "").split(" ")
                out = []
                for x in tweet:
                    if "#" not in x:
                        out.append(x)
                writer.writerow({"Date": transform_date(row["date"], row["time"]), "Location": get_user_location(row["username"], i), "Tweet": " ".join(" ".join(out).splitlines()),
                        "Hashtags": row["hashtags"].replace("]", "").replace("[", ""), "Retweets": row["retweets_count"],
                        "Likes": row["likes_count"]})


write_data()
