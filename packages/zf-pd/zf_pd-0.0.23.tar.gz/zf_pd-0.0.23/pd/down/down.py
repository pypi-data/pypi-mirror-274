from click import group
from click import option
from loguru import logger
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from re import sub as re_sub


@group(name='down', help="Download from the internet")
def down():
    pass


@down.command(help="Download a YouTube video")
@option('-l', '--link', type=str, required=True, prompt=True,
        help="Link to the YouTube video (e.g. https://www.youtube.com/watch?v=...)")
@option('-f', '--format', type=str, required=True, prompt=True,
        help="Format to download as (e.g. mp4, mp3, txt)")
def youtube(link: str, format: str):
    logger.debug("down video")

    if format == 'mp4':
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download()
    elif format == 'webm':
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        stream.download()
    elif format == 'txt':
        title, script = get_script(link)
        with open(f"{title}.txt", 'w') as f:
            f.write(script)
    else:
        logger.error(f"Unsupported format {format}")


def get_script(url: str) -> (str, str):
    yt = YouTube(url)
    title = re_sub(r'[\/:*?"<>|]', '', yt.title)

    if 'youtube.com' in url:
        url = url.split('=')[-1]

    subtitles = YouTubeTranscriptApi.get_transcript(url)

    script = " ".join([f"{sub['text']}" for sub in subtitles])
    return title, script


if __name__ == '__main__':
    link = f"https://www.youtube.com/watch?v=DxREm3s1scA"
    t, s = get_script(link)
    logger.info(f"{t}: {s}")
