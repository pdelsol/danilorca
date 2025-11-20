import json
import os.path
import re
import subprocess

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
    except botocore.exceptions.NoCredentialsError:
        # No AWS credentials available, assume file doesn't exist
        return False
    else:
        return True


def is_podcast_in_content(day):
    return os.path.isfile(f"content/{day}.md")


def upload_files_to_s3(day):
    try:
        s3 = boto3.resource("s3")
        s3.meta.client.upload_file(
            f"downloads/{day}.mp3",
            "s.danilorca.com",
            f"{day}.mp3",
            ExtraArgs={"ContentType": "audio/mpeg"},
        )
    except botocore.exceptions.NoCredentialsError:
        print(f"{day}: WARNING: No AWS credentials, skipping S3 upload")


def download_podcast(day, title, mp3_remote):
    mp3_local = f"downloads/{day}.mp3"
    if not is_podcast_in_s3(day):
        print(f"{day}: Download")
        response = requests.get(mp3_remote, stream=True)
        response.raise_for_status()
        with open(mp3_local, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        download_data(day, title)
        upload_files_to_s3(day)
    if not is_podcast_in_content(day):
        print(f"{day}: Write post")
        write_post(day, title)
    else:
        print(f"{day}: Skip")


def download_youtube():
    command = """
        yt-dlp -f "bestvideo+bestaudio/best" \
        --merge-output-format mp4 \
        --ignore-errors \
        --concurrent-fragments 10 \
        --downloader-args "ffmpeg:-hwaccel videotoolbox" \
        --no-keep-video \
        --no-overwrites \
        --output "%(upload_date>%Y-%m-%d)s %(title)s (%(id)s).%(ext)s" \
        "https://www.youtube.com/playlist?list=PLLFg6C6vW-3MIV54VGs7sx-_eBIdWK8dO"
    """
    subprocess.run(command, shell=True)


def download_data(day, podcast):
    json_local = f"downloads/{day}.json"
    with open(json_local, "w", encoding="utf8") as outfile:
        json.dump(podcast, outfile, indent=2, sort_keys=True)


headers = {"User-Agent": "Mozilla/5.0"}
page = requests.get(
    "https://www.radioagricultura.cl/episodios-completos/en-prendete/",
    headers=headers,
)
soup = BeautifulSoup(page.content, "html.parser")
# Find all figure elements that contain the main-article-box-card class
for episode in soup.select("figure.main-article-box-card"):
    # Find the title link
    title_link = episode.find("a", {"class": "main-article-box-card__permalink"})
    if not title_link:
        continue

    title = title_link.get_text().strip()
    episode_url = title_link["href"]

    # Extract date from URL (format: _YYYYMMDD)
    # Example: en-prendete-sabado-08-noviembre-2025_20251108/
    date_match = re.search(r"_(\d{8})", episode_url)
    if not date_match:
        print(f"ERROR: Could not extract date from URL: {episode_url}")
        continue

    date_str = date_match.group(1)  # YYYYMMDD format
    day = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"  # Convert to YYYY-MM-DD

    print(f"{day}: {title}")
    episode_page = requests.get(episode_url)
    episode_soup = BeautifulSoup(episode_page.content, "html.parser")
    if episode_soup.find("audio"):
        if episode_soup.find("audio") is not None and episode_soup.find(
            "audio"
        ).has_attr("src"):
            mp3_link = episode_soup.find("audio")["src"]
        elif episode_soup.find("audio").find("source") and episode_soup.find(
            "audio"
        ).find("source").has_attr("src"):
            mp3_link = episode_soup.find("audio").find("source")["src"]
        else:
            print(f"{day}: ERROR: COULDNT FIND AUDIO FILE")
            continue
        if "mp3" not in mp3_link:
            print(f"{day}: ERROR: FILE IS NOT MP3")
            continue
        download_podcast(day, title, mp3_link)
