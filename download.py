import requests
import json
import ipdb
from datetime import date
from dateutil.relativedelta import relativedelta
from urllib.request import urlretrieve
from urllib.parse   import quote
from os import path

HISTORIC = True
LIMIT = 20
BASE_URL = f"https://www.radioagricultura.cl/search/?type=podcast&format=json&programa=enprendete&limit={LIMIT}"

date_end = date(date.today().year, date.today().month, 1)

if HISTORIC:
    date_start = date(2021, 1, 1)
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
            day = podcast['url'][41:51].replace("/","-")
            with open(f"downloads/{day}.json", 'w') as outfile:
                json.dump(podcast, outfile)
            mp3_remote = podcast['contenido']
            mp3_local = f"downloads/{day}.mp3"
            if not path.exists(mp3_local) or path.getsize(mp3_local) < 20000000:
                print(f"ADD: {day}")
                urlretrieve(f"{mp3_remote[:7]}{quote(mp3_remote[7:])}", mp3_local)
            else:
                print(f"SKIP: {day}")
    date_current += relativedelta(months=1)
