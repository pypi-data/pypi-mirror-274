from os import getenv
from os import path as os_path
from typing import List

from boto3 import client as boto3_client
from click import group
from click import option
from loguru import logger

from ..config.config import add_instances
from ..config.config import load_pdconfig
from ..config.config import remove_instance
from ..config.config import update_instance
from ..model.model import Instance
from ..model.model import PD_CONFIG_FILE

AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = getenv('AWS_DEFAULT_REGION')


@group(name='ec2', help="Manage EC2 instances")
def ec2():
    logger.debug("ec2")
    if (
            AWS_ACCESS_KEY_ID is None or AWS_ACCESS_KEY_ID == '' or
            AWS_SECRET_ACCESS_KEY is None or AWS_SECRET_ACCESS_KEY == '' or
            AWS_DEFAULT_REGION is None or AWS_DEFAULT_REGION == ''
    ):
        print("Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION")
    return


@ec2.command(help="Launch an EC2 instance")
@option('-n', '--name', type=str, required=True, prompt=True,
        help="Name of the EC2 instance e.g. ec2-test")
@option('-c', '--count', type=int, default=1,
        help="Number of instances to launch")
@option('-p', '--project', type=str, default="",
        help="Project name e.g /path/to/project")
def launch(name, count, project):
    logger.debug("ec2 launch")

    if count > 1:
        logger.warning(f"{count} instances are being launched...")
        input("Press Enter to continue...")
    if project != "":
        if not os_path.isabs(project):
            logger.error(f"Project path {project} is not absolute")
            return
        if not os_path.exists(project):
            logger.error(f"Project {project} does not exist on disk")
            return

    # Load config.
    config = load_pdconfig()

    if 'ec2' not in config or len(config['ec2']) == 0:
        print(f"EC2 config not found, please update {PD_CONFIG_FILE}[ec2]")
        return

    ec2_config = config['ec2']
    if all(k in ec2_config for k in ('launch-template-id', 'key-pair-path')) is False:
        print(f"EC2 config is missing fields, please update {PD_CONFIG_FILE}[ec2]")
        return

    launch_template_id = config['ec2']['launch-template-id']
    key_pair_name = config['ec2']['key-pair-path'].split('/')[-1]
    if key_pair_name.endswith('.pem'):
        key_pair_name = key_pair_name[:-4]

    instances = launch_instances(
        launch_template_id=launch_template_id,
        key_pair_name=key_pair_name,
        instance_name=name,
        count=count
    )
    if len(instances) == 0:
        print("Failed to launch EC2 instances")
        return

    if count == 1:
        print(f"Launched 1 EC2 Instance: {instances[0]}")
    else:
        print(f"Launched {count} EC2 Instances: {instances}")

    add_instances(
        instances=instances,
        project=None if project == "" else project
    )


@ec2.command(help="Connect to an EC2 instance")
@option('-i', '--instance-id', type=str, required=True, prompt=True,
        help="ID of the EC2 instance to connect to e.g. i-1234567890abcdef")
def connect(instance_id):
    logger.debug("ec2 connect")


@ec2.command(help="Allocate an Elastic IP Address")
@option('-i', '--instance-id', type=str, required=True, prompt=True,
        help="ID of the EC2 instance to allocate an EIP for e.g. i-1234567890abcdef")
@option('-p', '--project', type=str, default="",
        help="Project name e.g /path/to/project")
def allocate(instance_id, project):
    logger.debug("ec2 allocate")

    public_ip = create_and_associate_eip(instance_id)
    if public_ip == "":
        print("Failed to allocate EIP")
        return

    print(f"Allocated EIP: {public_ip}")

    update_instance(
        instance=Instance(id=instance_id, ip=public_ip),
        project=None if project == "" else project
    )


@ec2.command(help="Terminate an EC2 instance")
@option('-i', '--instance-id', type=str, required=True, prompt=True,
        help="ID of the EC2 instance to terminate e.g. i-1234567890abcdef")
@option('-p', '--project', type=str, default="",
        help="Project name e.g /path/to/project")
def terminate(instance_id, project):
    logger.debug("ec2 terminate")

    if project != "":
        if not os_path.isabs(project):
            logger.error(f"Project path {project} is not absolute")
            return
        if not os_path.exists(project):
            logger.error(f"Project {project} does not exist on disk")
            return

    logger.info(f"Terminating EC2 Instance {instance_id}")
    input("Press Enter to continue...")

    ec2_client = boto3_client('ec2')

    try:
        response = ec2_client.terminate_instances(
            InstanceIds=[instance_id]
        )
        instances_data = response['TerminatingInstances']
        if len(instances_data) == 0:
            print("Failed to terminate EC2 instance")
            return

        instance_id = instances_data[0]['InstanceId']
        logger.debug(f"Terminated 1 EC2 instance with ID: {instance_id}")
        print(f"Terminated 1 EC2 instance with ID: {instance_id}")
    except Exception as e:
        msg = f"Failed to terminate EC2 instance due to {e}"
        logger.error(msg)
        print("Failed to launch EC2 instance")

    remove_instance(
        instance_id=instance_id,
        project=None if project == "" else project
    )


def launch_instances(
        launch_template_id: str,
        key_pair_name: str,
        instance_name: str,
        count: int,
) -> List[Instance]:
    if count < 1:
        logger.error("Count must be greater than 0")
        return []

    ec2_client = boto3_client('ec2')

    try:
        # Launch an EC2 instance using the specified launch template, security group, and key pair
        response = ec2_client.run_instances(
            LaunchTemplate={'LaunchTemplateId': launch_template_id},
            KeyName=key_pair_name,
            MinCount=count,
            MaxCount=count,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ]
        )

        # Extract the instance ID from the response
        instances_data = response['Instances']
        instance_ids = [instance['InstanceId'] for instance in instances_data]

        instances: List[Instance] = []
        for instance_id in instance_ids:
            instances.append(Instance(id=instance_id, ip=""))

        logger.debug(f"Launched {len(instances)} instance: {instances}")
        return instances
    except Exception as e:
        msg = f"Failed to launch EC2 Instances due to {e}"
        logger.error(msg)
        return []


def create_and_associate_eip(instance_id: str) -> str:
    if instance_id is None or instance_id == "":
        logger.error("Instance ID is required")
        return ""

    ec2_client = boto3_client('ec2')

    # Allocate a new Elastic IP Address
    allocation = ec2_client.allocate_address(Domain='vpc')
    eip_address = allocation['PublicIp']
    logger.debug(f"Allocated EIP: {eip_address}")

    # Associate the EIP with the specified EC2 instance
    allocation_id = allocation['AllocationId']
    ec2_client.associate_address(
        InstanceId=instance_id,
        AllocationId=allocation_id
    )
    logger.debug(f"Associated EIP {eip_address} with EC2 Instance {instance_id}")

    return eip_address
