from importlib import resources
from re import compile as re_compile

from click import group
from click import option
from jinja2 import BaseLoader
from jinja2 import Environment
from loguru import logger


@group(name='nginx', help="Manage nginx files")
def nginx():
    pass


@nginx.command(help="Generate nginx config")
@option('-h', '--host', type=str, required=True, default='localhost',
        help="Host to proxy to e.g. localhost")
@option('-p', '--port', type=int, required=True, default=80,
        help="Port to proxy to e.g. 80")
@option('-d', '--domain', type=str, required=True, default='example.com',
        help="Domain to use for nginx config e.g. example.com")
@option('-s', '--static', type=str, default='',
        help="Static resources path e.g. /path/to/static")
def generate(host: str, port: int, domain: str, static: str):
    logger.debug("nginx generate")

    re_scheme = re_compile(r'^https?://')

    scheme = 'http'
    if host.startswith('https://'):
        scheme = 'https'
    host = re_scheme.sub('', host)
    if port < 0 or port > 65535:
        logger.error("invalid port")
        return
    domain = re_scheme.sub('', domain)

    template_name = 'simple.com' if static == '' else 'static.com'
    template_str = resources.read_text('pd.nginx.templates', template_name)

    logger.debug(f"scheme: {scheme}")
    logger.debug(f"host: {host}")
    logger.debug(f"port: {port}")
    logger.debug(f"domain: {domain}")
    logger.debug(f"template_str: {template_str}")

    j2_env = Environment(loader=BaseLoader())
    template = j2_env.from_string(template_str)
    args = {
        'scheme': scheme,
        'host': host,
        'port': port,
        'domain': domain,
    }
    if static != '':
        args['static'] = static
    output = template.render(**args)
    print(f"/etc/nginx/sites-available/{domain}")
    print(output)
    return
