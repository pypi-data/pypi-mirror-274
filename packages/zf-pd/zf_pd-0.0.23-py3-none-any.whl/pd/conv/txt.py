from loguru import logger
from os import getenv
from openai import OpenAI
from typing import Dict, Literal


def txt(src: str, dst: str, opts: Dict[str, str]) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == 'mp3':
        txt_to_mp3(src, dst, opts)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def txt_to_mp3(src: str, dst: str, opts: Dict[str, str]) -> None:
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        logger.error("OPENAI_API_KEY is not set")
        return

    client = OpenAI()

    args = {"model": "tts-1", "voice": opts.get("voice", "echo"), "input": src}
    response = client.audio.speech.create(**args)

    # Save to disk.
    with open(dst, "wb") as file:
        file.write(response.read())

    return
