from moviepy.editor import VideoFileClip
from os import path as os_path
from loguru import logger


def mp4(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == 'mp3':
        mp4_to_mp3(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def mp4_to_mp3(src: str, dst: str) -> None:
    video = VideoFileClip(src)
    audio = video.audio
    audio.write_audiofile(dst)
    return
