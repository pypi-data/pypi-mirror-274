from os import path as os_path

from loguru import logger
from setuptools import find_packages
from setuptools import setup


def read_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), 'pd', 'version.py')
    with open(version_file) as file:
        exec(file.read())
    version = locals()['__version__']
    logger.debug(f"Building {PACKAGE_NAME} v{version}")
    return version


PACKAGE_NAME = 'zf-pd'
PACKAGE_VERSION = read_version()
AUTHOR_NAME = 'zeffmuks'
AUTHOR_EMAIL = 'zeffmuks@gmail.com'

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='pd supercharges your development workflows',
    long_description=read_long_description(),  # This is the important part
    long_description_content_type='text/markdown',  # This tells PyPI the content is in Markdown
    include_package_data=True,
    package_data={
        'pd.config': ['templates/*'],
        'pd.init': ['templates/pd-fastapi/*', 'templates/pd-react/*', 'templates/pd-nextjs/*',
                    'templates/pd-electron/*'],
        'pd.nginx': ['templates/*'],
    },
    install_requires=[
        "wheel",
        "loguru",
        "click",
        "setuptools",
        "jinja2",
        "moviepy",
        "pydantic",
        "pydub",
        "moviepy"
        "openai",
        "img2pdf",
        "PyPDF2",
        "reportlab",
        "pytube",
        "youtube_transcript_api",
        "boto3"
    ],
    packages=find_packages(
        include=['pd', 'pd.*'],
        exclude=['venv', 'venv.*']
    ),
    entry_points={
        'console_scripts': [
            'pd=pd.__main__:main'  # Invokes pd/__main__.py::main()
        ]
    },
)
