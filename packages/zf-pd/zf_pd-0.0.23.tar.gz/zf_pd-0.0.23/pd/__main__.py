from sys import stderr

from click import group
from click import version_option
from loguru import logger

from pd.config.config import config
from pd.conv.conv import conv
from pd.down.down import down
from pd.ec2.ec2 import ec2
from pd.env.env import env
from pd.init.init import init
from pd.nginx.nginx import nginx
from pd.sync.sync import sync
from pd.version import __version__


@group()
@version_option(__version__, '-v', '--version', help='Show the version and exit')
def cli():
    pass


cli.add_command(config)
cli.add_command(conv)
cli.add_command(down)
cli.add_command(ec2)
cli.add_command(init)
cli.add_command(nginx)
cli.add_command(sync)
cli.add_command(env)


def main():
    logger.remove(0)
    logger.add(stderr, level="DEBUG")
    cli()


if __name__ == "__main__":
    main()
