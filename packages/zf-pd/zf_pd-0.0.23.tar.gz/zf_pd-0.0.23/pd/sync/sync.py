from click import group
from loguru import logger


@group(name='sync', help="Sync files")
def sync():
    pass


@sync.command()
def zshrc():
    logger.debug("sync .zshrc")


@sync.command()
def vimrc():
    logger.debug("sync .vimrc")


@sync.command()
def gitconfig():
    logger.debug("sync .gitconfig")
