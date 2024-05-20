from PIL import Image
from moviepy.editor import ImageClip

from loguru import logger


def to_png(src: str) -> str:
    ext = src.split(".")[-1]
    dst = src.replace(f".{ext}", ".png")

    with Image.open(src) as image:
        image.save(dst, "PNG")

    logger.debug(f"Converted {src} to {dst}")

    return dst


def png(src: str, dst: str, duration: int) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == 'mp4':
        png_to_mp4(src, dst, duration)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def png_to_mp4(src: str, dst: str, duration: int) -> None:
    logger.debug(f"Converting {src} to {dst} of {duration} seconds")

    clip = ImageClip(src, duration=duration)
    clip.write_videofile(dst, fps=24, codec='libx264')
    return
