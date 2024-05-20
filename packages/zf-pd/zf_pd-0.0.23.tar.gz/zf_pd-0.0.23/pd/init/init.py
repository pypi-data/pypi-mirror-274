from importlib import resources
from os import path as os_path
from shutil import copytree
from shutil import ignore_patterns

from click import group
from click import option
from loguru import logger

from ..config.config import manage_projects


@group(name='init', help="Initialize a new project")
def init():
    pass


@init.command(help="Start a new FastAPI App")
@option('-n', '--name', type=str, required=True, prompt=True,
        help="Project name e.g. project (or /path/to/project)")
@option('-f', '--force', type=bool, is_flag=True, default=False,
        help="Force overwrite of existing files")
def fastapi(name: str, force: bool):
    logger.debug("init fastapi")

    path, name = (name.rsplit('/', 1) if '/' in name else (".", name))
    full_path = os_path.join(path, name)

    if not force:
        if os_path.exists(full_path):
            logger.error(f"Path {full_path} already exists")
            return

    logger.debug(f"path: {path}")
    logger.debug(f"name: {name}")
    logger.debug(f"full_path: {full_path}")

    ignore_dirs = ignore_patterns('.idea', '__pycache__', 'venv', 'node_modules')
    with resources.path('pd.init.templates', 'pd-fastapi') as template_path:
        logger.debug(f"Copying {template_path} to {full_path}")
        copytree(template_path, full_path, dirs_exist_ok=force, ignore=ignore_dirs)

    manage_projects(add=f"fastapi,{full_path}")

    print(f'Created project {name} at {full_path}. Please run the following commands:')
    print("cd", full_path)
    print("pip install -r requirements.txt")
    print("npm install")
    print("python -m uvicorn app.main:app --reload")
    print("Open http://localhost:8000")
    return


@init.command(help="Start a new React App")
@option('-n', '--name', type=str, required=True, prompt=True,
        help="Project name e.g. project (or /path/to/project)")
@option('-f', '--force', type=bool, is_flag=True, default=False,
        help="Force overwrite of existing files")
def react(name: str, force: bool):
    logger.debug("init react")

    path, name = (name.rsplit('/', 1) if '/' in name else (".", name))
    full_path = os_path.join(path, name)

    if not force:
        if os_path.exists(full_path):
            logger.error(f"Path {full_path} already exists")
            return

    logger.debug(f"path: {path}")
    logger.debug(f"name: {name}")
    logger.debug(f"full_path: {full_path}")

    ignore_dirs = ignore_patterns('.idea', 'node_modules')
    with resources.path('pd.init.templates', 'pd-react') as template_path:
        logger.debug(f"Copying {template_path} to {full_path}")
        copytree(template_path, full_path, dirs_exist_ok=force, ignore=ignore_dirs)

    manage_projects(add=f"react,{full_path}")

    print(f'Created project {name} at {full_path}. Please run the following commands:')
    print(full_path)
    print("cd", full_path)
    print("npm install")
    print("npm start dev")
    print("Open http://localhost:3000")
    return


@init.command(help="Start a new NextJS App")
@option('-n', '--name', type=str, required=True, prompt=True,
        help="Project name e.g. project (or /path/to/project)")
@option('-f', '--force', type=bool, is_flag=True, default=False,
        help="Force overwrite of existing files")
def nextjs(name: str, force: bool):
    logger.debug("init nextjs")

    path, name = (name.rsplit('/', 1) if '/' in name else (".", name))
    full_path = os_path.join(path, name)

    if not force:
        if os_path.exists(full_path):
            logger.error(f"Path {full_path} already exists")
            return

    logger.debug(f"path: {path}")
    logger.debug(f"name: {name}")
    logger.debug(f"full_path: {full_path}")

    ignore_dirs = ignore_patterns('.idea', '.next', 'node_modules')
    with resources.path('pd.init.templates', 'pd-nextjs') as template_path:
        logger.debug(f"Copying {template_path} to {full_path}")
        copytree(template_path, full_path, dirs_exist_ok=force, ignore=ignore_dirs)

    manage_projects(add=f"nextjs,{full_path}")

    print(f'Created project {name} at {full_path}. Please run the following commands:')
    print("cd", full_path)
    print("npm install")
    print("npm run dev")
    print("Open http://localhost:3000")
    return


@init.command(help="Start a new Electron App")
@option('-n', '--name', type=str, required=True, prompt=True,
        help="Project name e.g. project (or /path/to/project)")
@option('-f', '--force', type=bool, is_flag=True, default=False,
        help="Force overwrite of existing files")
def electron(name: str, force: bool):
    logger.debug("init electron")

    path, name = (name.rsplit('/', 1) if '/' in name else (".", name))
    full_path = os_path.join(path, name)

    if not force:
        if os_path.exists(full_path):
            logger.error(f"Path {full_path} already exists")
            return

    logger.debug(f"path: {path}")
    logger.debug(f"name: {name}")
    logger.debug(f"full_path: {full_path}")

    ignore_dirs = ignore_patterns('.idea', 'node_modules')
    with resources.path('pd.init.templates', 'pd-electron') as template_path:
        logger.debug(f"Copying {template_path} to {full_path}")
        copytree(template_path, full_path, dirs_exist_ok=force, ignore=ignore_dirs)

    manage_projects(add=f"electron,{full_path}")

    print(f'Created project {name} at {full_path}. Please run the following commands:')
    print(full_path)
    print("cd", full_path)
    print("npm install")
    print("npm start")
    return
