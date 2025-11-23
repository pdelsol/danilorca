yt-dlp -f "bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  --ignore-errors \
  --concurrent-fragments 10 \
  --downloader-args "ffmpeg:-hwaccel videotoolbox" \
  --no-keep-video \
  --no-overwrites \
  --output "%(upload_date>%Y-%m-%d)s %(title)s (%(id)s).%(ext)s" \
  "https://www.youtube.com/playlist?list=PLLFg6C6vW-3MIV54VGs7sx-_eBIdWK8dO"
  