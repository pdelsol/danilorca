import requests
import json
import ipdb
from datetime import date
from dateutil.relativedelta import relativedelta
from urllib.request import urlretrieve
from urllib.parse   import quote
from os import path

HISTORIC = True
BASE_URL = "https://www.radioagricultura.cl/search/?type=podcast&format=json&programa=enprendete&limit=20"

def write_post(day, podcast):
    content = (
        f"Title: {podcast['titulo']}\n"
        f"Date: {day}\n"
        f"Category: Podcast\n"
        f"Mp3: https://s.danilorca.com/{day}.mp3\n"
        f"\n"
        f"<a href=\"https://s.danilorca.com/{day}.mp3\" type=\"audio/mpeg\">\n"
        f"Escuchar\n"
        f"</a>\n"
    )
    f = open(f"content/{day}.md", "w")
    f.write(content)
    f.close()


def download_mp3(day, podcast):
    mp3_remote = podcast["contenido"]
    mp3_local = f"downloads/{day}.mp3"
    if not path.exists(mp3_local) or path.getsize(mp3_local) < 20000000:
        print(f"ADD: {day}")
        urlretrieve(f"{mp3_remote[:7]}{quote(mp3_remote[7:])}", mp3_local)
    else:
        print(f"SKIP: {day}")

def download_content(day, podcast):
    json_local = f"downloads/{day}.json"
    with open(json_local, "w") as outfile:
        json.dump(podcast, outfile, indent=2, sort_keys=True)
    write_post(day, podcast)


date_end = date(date.today().year, date.today().month, 1)

if HISTORIC:
    date_start = date(2020, 5, 1)
else:
    date_start = date_end - relativedelta(months=1)

date_current = date_start
while date_current <= date_end:
    URL = f"{BASE_URL}&year={date_current.year}&month={date_current.month}"
    print(f"-- {date_current} --")
    response = requests.get(URL)
    if response.status_code == 200:
        podcasts = response.json()['post']
        for podcast in podcasts:
            day = podcast["url"][41:51].replace("/","-")
            download_content(day, podcast)
            download_mp3(day, podcast)
    date_current += relativedelta(months=1)
