# danilorca.com

100% serverless static site builder and deployer.

Setup that syncs mp3 files from a radio website in the internet and publishes it them to a rss podcast.

Uses github actions to run weekly cron to update content, creates a branch, builds the site and deplpys it to a new cloudflare page as stage to review.

Onced reviewed, you merge and it deploys the master cloudflare pages with http page and rss podcast feed.

Mp3s are uploaded to a s3 bucket.

## developing
### deps

```bash
uv sync
```
## create static site

```
pelican content
pelican --listen
```

## updating content

### download new radio episodes

```
uv run python download.c
aws s3 sync downloads/ s3://s.danilorca.com/
```

## deploy
```
git push
```

publishes to spotify

https://creators.spotify.com/

publishes to apple

https://podcastsconnect.apple.com/
