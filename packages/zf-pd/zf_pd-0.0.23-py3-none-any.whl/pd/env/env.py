from os import path as os_path

from click import group
from click import option
from loguru import logger


@group(name='env', help="Manage environments")
def env():
    pass


@env.command(help="Show an environment")
@option('-n', '--name', type=str, required=True, prompt=True,
        help='Name of the environment e.g. zsh, vim, git')
def show(name):
    logger.debug("env view")

    env_name = {
        'zsh': 'zshrc',
        'vim': 'vimrc',
        'git': 'gitconfig',
        'tmux': 'tmux.conf',
    }
    if name not in env_name:
        logger.error(f"Unknown environment {name}")
        return

    env_path = os_path.expanduser(f"~/.{env_name[name]}")
    logger.debug(f"env_path: {env_path}")

    if not os_path.exists(env_path):
        logger.error(f"Environment {name} not found")
        return

    with open(env_path, 'r') as f:
        print(f.read())
    return


@env.command(help="Sync an environment")
@option('-n', '--name', type=str, required=True, prompt=True,
        help='Name of the environment e.g. zsh, vim, git')
def sync(name):
    logger.debug("env sync")
    return
