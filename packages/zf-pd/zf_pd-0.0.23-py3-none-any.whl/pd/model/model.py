from os import path as os_path

from pydantic import BaseModel

PD_CONFIG_FILE = os_path.expanduser('~/.pdconfig.json')


class Project(BaseModel):
    """
    Each project is uniquely identified by its full path on disk
    """

    type: str  # Type of project (e.g. react, fastapi)
    name: str  # Name of the project (e.g. project)
    path: str  # Full path on disk (e.g. /path/to/project)


class Instance(BaseModel):
    """
    Each instance is uniquely identified by its ID
    """

    id: str  # Instance ID
    ip: str  # Instance IP (e.g. Elastic IP)
