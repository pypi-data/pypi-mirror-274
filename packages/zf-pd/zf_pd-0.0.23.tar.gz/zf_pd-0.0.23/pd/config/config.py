from importlib import resources
from json import dump as json_dump
from json import dumps as json_dumps
from json import load as json_load
from os import path as os_path
from typing import Dict
from typing import List

from click import group
from click import option
from jinja2 import BaseLoader
from jinja2 import Environment
from jinja2 import FileSystemLoader
from loguru import logger

from ..model.model import Instance
from ..model.model import PD_CONFIG_FILE

jinja2_env = Environment(loader=FileSystemLoader('./templates'))


def load_pdconfig() -> Dict:
    if not os_path.exists(PD_CONFIG_FILE):
        return {"projects": []}

    with open(PD_CONFIG_FILE, 'r') as file:
        data = json_load(file)
        file.close()
        return data


def save_pdconfig(data: Dict):
    with open(PD_CONFIG_FILE, 'w') as file:
        json_dump(data, file, indent=4)
        file.close()
    logger.debug(f"Saved config to {PD_CONFIG_FILE}")
    return


@group(name='config', help="Manage your config")
def config():
    if not os_path.exists(PD_CONFIG_FILE):
        with open(PD_CONFIG_FILE, 'w') as file:
            json_dump({"projects": [], "ec2": {}}, file, indent=4)
            file.close()
    return


@config.command(help="Show the config")
@option('-s', '--select', type=str, default="",
        help="Select the config to show e.g. ec2, projects")
def show(select):
    logger.debug("config show")
    data = load_pdconfig()

    if select == "":
        data_string = json_dumps(data, indent=4)
        print(data_string)
    elif select == "ec2":
        if 'ec2' in data:
            data_string = json_dumps(data['ec2'], indent=4)
            print(data_string)
        else:
            print("No EC2 config found")
    elif select == "projects":
        if 'projects' in data:
            data_string = json_dumps(data['projects'], indent=4)
            print(data_string)
        else:
            print("No projects found")
    return


@config.command(help="Create config for a project")
@option('-t', '--type', type=str, prompt=True,
        help="Config type e.g. zsh, ")
@option('-p', '--project', type=str, prompt=True,
        help="Project path e.g. /path/to/project")
@option('-d', '--domain', type=str, default="",
        help="Domain name e.g. example.com")
def create(type: str, project: str, domain: str):
    logger.debug("config create")

    if type == "zsh":
        config_name = ".zshrc"
        config_path = os_path.expanduser(f"~/{config_name}")
        if not os_path.exists(config_path):
            logger.error(f"Config file {config_path} not found")
            return

        project_config: List[str] = []
        lines: List[str] = open(config_path, 'r').readlines()
        for line in lines:
            if line.startswith(f"export {project.upper()}"):
                logger.debug(f"Matched {line}")
                project_config.append(line.strip())

        # Load template
        template_str = resources.read_text('pd.config.templates', 'zshrc.j2')
        j2_env = Environment(loader=BaseLoader())
        template = j2_env.from_string(template_str)
        args = {
            'config': "\n".join(project_config),
        }
        if domain != "":
            args['domain_export'] = f'export SITE_NAME="{domain}"'
        output = template.render(**args)
        print("~/.zshrc")
        print(output)
    return


@config.command(help="Manage your projects")
@option('-a', '--add', type=str, default="",
        help="Add a project e.g. react,/path/to/project")
@option('-d', '--delete', type=str, default="",
        help="Delete a project e.g. /path/to/project")
def projects(add: str, delete: str):
    manage_projects(add, delete)
    return


def manage_projects(
        add: str = "",
        delete: str = "",
):
    data = load_pdconfig()

    if add is not None and add != "":
        logger.debug("projects add")

        try:
            ptype, path, name, full_path = validate_project(add)
        except Exception as e:
            logger.error(e)
            return

        for project in data['projects']:
            if project['path'] == full_path:
                logger.debug(f"Project {project['path']} already added")
                return

        data['projects'].append(
            {
                "type": ptype,
                "name": name,
                "path": full_path,
            }
        )

    if delete is not None and delete != "":
        logger.debug("projects delete")

        for project in data['projects']:
            if project['path'] == delete:
                logger.debug(f"Deleting {project['path']}")
                data['projects'].remove(project)
                return

        logger.error(f"Project {delete} not found")

    save_pdconfig(data)

    return


def validate_project(project_str: str):
    if ',' not in project_str:
        msg = f"Invalid format {project_str}, use <type>,<path>"
        raise Exception(msg)

    ptype, ppath = project_str.split(',', 1)

    valid_ptypes = ["react", "fastapi", "electron", "nextjs"]

    # Validate project type
    if ptype not in valid_ptypes:
        msg = f"Invalid project type {ptype}, use one of {valid_ptypes}"
        raise Exception(msg)

    # Validate project path
    path, name = (ppath.rsplit('/', 1) if '/' in ppath else (".", ppath))
    if path == ".":  # Expand path
        path = os_path.abspath(path)
    full_path = os_path.join(path, name)

    if not os_path.exists(full_path):
        msg = f"Path {full_path} does not exist, please create it first"
        raise Exception(msg)

    logger.debug(f"ptype: {ptype}")
    logger.debug(f"path: {path}")
    logger.debug(f"name: {name}")
    logger.debug(f"full_path: {full_path}")

    return ptype, path, name, full_path


def add_instances(
        instances: List[Instance],
        project: str = None
) -> None:
    if len(instances) == 0:
        logger.error("No Instances provided")
        return

    # Load config
    data = load_pdconfig()
    if 'ec2' not in data:
        data['ec2'] = {}
    if 'instances' not in data['ec2']:
        data['ec2']['instances'] = []

    # Add Instances to EC2
    for instance in instances:
        exists = False
        for pd_ec2_instance in data['ec2']['instances']:
            if 'instance-id' in pd_ec2_instance and pd_ec2_instance['instance-id'] == instance.id:
                exists = True
                break

        if not exists:
            logger.debug(f"Adding {instance.id} to {PD_CONFIG_FILE}[ec2][instances]")
            data['ec2']['instances'].append(
                {
                    "instance-id": instance.id,
                    "instance-ip": instance.ip,
                }
            )

    # Add Instances to Project
    if project is not None and project != "":
        for p in data['projects']:
            if p['path'] == project:
                if 'instances' not in p:
                    pd_project_instances: List[Dict[str, str]] = []
                    for instance in instances:
                        pd_project_instances.append(
                            {
                                "instance-id": instance.id,
                                "instance-ip": instance.ip,
                            }
                        )
                    p['instances'] = pd_project_instances
                    return

                for instance in instances:
                    exists = False
                    for pd_project_instance in p['instances']:
                        if 'instance-id' in pd_project_instance and pd_project_instance['instance-id'] == instance.id:
                            exists = True
                            break

                    if not exists:
                        logger.debug(f"Adding {instance.id} to {PD_CONFIG_FILE}[projects][{project}][instances]")
                        p['instances'].append(
                            {
                                "instance-id": instance.id,
                                "instance-ip": instance.ip,
                            }
                        )

    save_pdconfig(data)
    return


def update_instance(
        instance: Instance,
        project: str = None
) -> None:
    # Load config
    data = load_pdconfig()
    if 'ec2' not in data or 'instances' not in data['ec2']:
        logger.error(f"No instances found in {PD_CONFIG_FILE}[ec2][instances]")
        return

    # Add Instances to EC2
    for pd_ec2_instance in data['ec2']['instances']:
        if 'instance-id' in pd_ec2_instance and pd_ec2_instance['instance-id'] == instance.id:
            logger.debug(f"Updating {instance.id} in {PD_CONFIG_FILE}[ec2][instances]")

            data['ec2']['instances'].remove(pd_ec2_instance)
            data['ec2']['instances'].append(
                {
                    "instance-id": instance.id,
                    "instance-ip": instance.ip,
                }
            )

    # Add Instances to Project
    if project is not None and project != "":
        for p in data['projects']:
            if p['path'] == project:
                if 'instances' not in p:
                    logger.error(f"No instances found in {PD_CONFIG_FILE}[projects][{project}][instances]")
                    return

                for pd_project_instance in p['instances']:
                    if 'instance-id' in pd_project_instance and pd_project_instance['instance-id'] == instance.id:
                        logger.debug(f"Updating {instance.id} in {PD_CONFIG_FILE}[projects][{project}][instances]")

                        p['instances'].remove(pd_project_instance)
                        p['instances'].append(
                            {
                                "instance-id": instance.id,
                                "instance-ip": instance.ip,
                            }
                        )

    save_pdconfig(data)
    return


def remove_instance(
        instance_id: str,
        project: str = None
) -> None:
    if instance_id == "":
        logger.error("No instance ID provided")
        return

    # Load config
    data = load_pdconfig()

    # Remove Instance from EC2
    if 'ec2' in data and 'instances' in data['ec2']:
        for pd_ec2_instance in data['ec2']['instances']:
            if 'instance-id' in pd_ec2_instance and pd_ec2_instance['instance-id'] == instance_id:
                logger.debug(f"Removing {instance_id} from {PD_CONFIG_FILE}[ec2][instances]")

                data['ec2']['instances'].remove(pd_ec2_instance)

    # Remove Instance from Project
    if project is not None and project != "":
        for p in data['projects']:
            if 'path' in p and 'instances' in p and p['path'] == project:
                for pd_project_instance in p['instances']:
                    if 'instance-id' in pd_project_instance and pd_project_instance['instance-id'] == instance_id:
                        logger.debug(f"Removing {instance_id} from {PD_CONFIG_FILE}[projects][{project}][instances]")

                        p['instances'].remove(pd_project_instance)

    save_pdconfig(data)
    return
