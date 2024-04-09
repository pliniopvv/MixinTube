import yt_dlp

ydl_opts = {}

class Youtube:
    def download(url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)