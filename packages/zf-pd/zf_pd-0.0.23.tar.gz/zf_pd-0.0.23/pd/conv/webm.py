from loguru import logger
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip


def webm(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == 'mp3':
        try:
            webm_video_to_mp3(src, dst)
        except Exception as e:
            logger.debug(f"Failed to convert {src} to {dst} as video, retrying as audio")
            webm_audio_to_mp3(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def webm_video_to_mp3(src: str, dst: str) -> None:
    video = VideoFileClip(src)
    audio = video.audio
    audio.write_audiofile(dst)
    return


def webm_audio_to_mp3(src: str, dst: str) -> None:
    audio = AudioFileClip(src)
    audio.write_audiofile(dst)
    return
