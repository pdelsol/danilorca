import json
import os.path
from urllib.request import urlretrieve

import boto3
import botocore
import requests
from bs4 import BeautifulSoup


def write_post(day, title):
    content = (
        f"Title: {title}\n"
        f"Date: {day}\n"
        f"Category: Podcast\n"
        f"Mp3: https://s.danilorca.com/{day}.mp3\n"
        f"Company: {title}\n"
        f"Person: {title}\n"
        f"Tags: {title}\n"
        f"Rating: 0\n"
        f"\n"
        f'<a href="https://s.danilorca.com/{day}.mp3" type="audio/mpeg">\n'
        f"Escuchar\n"
        f"</a>\n"
    )
    f = open(f"content/{day}.md", "w", encoding="utf8")
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


def is_podcast_in_content(day):
    return os.path.isfile(f"content/{day}.md")


def upload_files_to_s3(day):
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(
        f"downloads/{day}.mp3",
        "s.danilorca.com",
        f"{day}.mp3",
        ExtraArgs={"ContentType": "audio/mpeg"},
    )


def download_podcast(day, title, mp3_remote):
    mp3_local = f"downloads/{day}.mp3"
    if not is_podcast_in_s3(day):
        print(f"{day}: Download")
        urlretrieve(mp3_remote, mp3_local)
        download_data(day, title)
        upload_files_to_s3(day)
    if not is_podcast_in_content(day):
        print(f"{day}: Write post")
        write_post(day, title)
    else:
        print(f"{day}: Skip")


def download_data(day, podcast):
    json_local = f"downloads/{day}.json"
    with open(json_local, "w", encoding="utf8") as outfile:
        json.dump(podcast, outfile, indent=2, sort_keys=True)


page = requests.get("https://www.radioagricultura.cl/podcast_programas/en-prendete/")
soup = BeautifulSoup(page.content, "html.parser")
for episode in soup.find_all("article", {"class": "podcast"}):
    title = episode.find("h2").find("a").get_text()
    day = episode.find("time")["datetime"][:10]
    print(f"{day}: {title}")
    episode_page = requests.get(episode.find("h2").find("a")["href"])
    episode_soup = BeautifulSoup(episode_page.content, "html.parser")
    if episode_soup.find("audio"):
        if episode_soup.find("audio") is not None and episode_soup.find(
            "audio"
        ).has_attr("src"):
            mp3_link = episode_soup.find("audio")["src"]
        elif episode_soup.find("audio").find("source").has_attr("src"):
            mp3_link = episode_soup.find("audio").find("source")["src"]
        else:
            print(f"{day}: ERROR: COULDNT FIND AUDIO FILE")
            continue
        if "mp3" in mp3_link:
            download_podcast(day, title, mp3_link)
        else:
            print(f"ERROR: no mp3 file found for {day}")
