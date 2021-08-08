import json
from datetime import date
from urllib.parse import quote
from urllib.request import urlretrieve

import boto3
import botocore
import requests
from dateutil.relativedelta import relativedelta
from mutagen.mp3 import MP3

HISTORIC = False
BASE_URL = "https://www.radioagricultura.cl/search/?type=podcast&format=json&programa=enprendete&limit=20"


def write_post(day, duration, podcast):
    content = (
        f"Title: {podcast['titulo']}\n"
        f"Date: {day}\n"
        f"Category: Podcast\n"
        f"Mp3: https://s.danilorca.com/{day}.mp3\n"
        f"Company: {podcast['titulo']}\n"
        f"Person: {podcast['titulo']}\n"
        f"Tags: {podcast['titulo']}\n"
        f"\n"
        f'<a href="https://s.danilorca.com/{day}.mp3" type="audio/mpeg">\n'
        f"Escuchar\n"
        f"</a>\n"
    )
    f = open(f"content/{day}.md", "w")
    f.write(content)
    f.close()


def is_podcast_in_s3(day):
    s3 = boto3.resource("s3")
    try:
        s3.Object("s.danilorca.com", f"{day}.mp3").load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        return None  # Something else has gone wrong.
    else:
        return True


def upload_files_to_s3(day):
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(
        f"downloads/{day}.mp3",
        "s.danilorca.com",
        f"{day}.mp3",
        ExtraArgs={"ContentType": "audio/mpeg"},
    )
    s3.meta.client.upload_file(
        f"downloads/{day}.json",
        "s.danilorca.com",
        f"{day}.json",
        ExtraArgs={"ContentType": "application/json"},
    )


def download_podcast(day, podcast):
    mp3_remote = podcast["contenido"]
    mp3_local = f"downloads/{day}.mp3"
    if not is_podcast_in_s3(day):
        print(f"{day}: Download")
        urlretrieve(f"{mp3_remote[:7]}{quote(mp3_remote[7:])}", mp3_local)
        download_data(day, podcast)
        duration = get_mp3_duration(mp3_local)
        write_post(day, duration, podcast)
        upload_files_to_s3(day)
    else:
        print(f"{day}: Skip")


def get_mp3_duration(filepath):
    try:
        return int(MP3(filepath).info.length)
    except Exception:
        return None


def download_data(day, podcast):
    json_local = f"downloads/{day}.json"
    with open(json_local, "w") as outfile:
        json.dump(podcast, outfile, indent=2, sort_keys=True)


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
        podcasts = response.json()["post"]
        for podcast in podcasts:
            day = podcast["url"][41:51].replace("/", "-")
            download_podcast(day, podcast)
    date_current += relativedelta(months=1)
