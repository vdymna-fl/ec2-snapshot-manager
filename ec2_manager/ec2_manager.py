"""CLI to manage EC2 instances, volumes and snapshots."""

import boto3
import click
from ec2_manager import constants
from ec2_manager.instance import InstanceManager


instance_manager = None

@click.group()
@click.option('--profile', default=None, help='Specify AWS profile name.')
@click.option('--region', default=None, help="Specify AWS region name.")
def cli(profile, region):
	"""CLI to manage EC2 instances, volumes and snapshots."""
	global instance_manager

	session_cfg = {}
	if profile:
		session_cfg['profile_name'] = profile
	if region:
		session_cfg['region_name'] = region

	session = boto3.Session(**session_cfg)
	
	instance_manager = InstanceManager(session)


@cli.group('instances')
def instances():
	"""Commands for instances."""


@instances.command('list')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
def list_instances(project):
	"""List EC2 instances."""

	for i in instance_manager.get_ec2_instances(project):
		tags = { t['Key']: t['Value'] for t in i.tags or []}

		print(', '.join([
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name or '<no public dns name>',
			tags.get(constants.PROJECT_TAG, '<no project>')
		]))
	
	return


@instances.command('start')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
@click.option('--instance', default=None, help="Specify an instance id")
def start_instances(project, instance):
	"""Start EC2 instances."""

	for i in instance_manager.get_ec2_instances(project, instance):
		if instance_manager.is_instance_stopped(i):
			print("Starting {0} instance...".format(i.id))
			i.start()
		else:
			print("Skipping {0} instance in {1} state".format(i.id, i.state['Name']))

	return


@instances.command('stop')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
@click.option('--instance', default=None, help="Specify an instance id")
def stop_instances(project, instance):
	"""Stop EC2 instances."""

	for i in instance_manager.get_ec2_instances(project, instance):
		try_stop_instance(i)

	return

@instances.command('reboot')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
@click.option('--instance', default=None, help="Specify an instance id")
def reboot_instances(project, instance):
	"""Reboot EC2 instances."""

	for i in instance_manager.get_ec2_instances(project, instance):
		if instance_manager.is_instance_running(i):
			print("Rebooting {0} instance...".format(i.id))
			i.reboot()
		else:
			print("Skipping {0} instance in {1} state".format(i.id, i.state['Name']))

	return


@instances.command('snapshot')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
@click.option('--instance', default=None, help="Specify an instance id")
def create_snapshots(project, instance):
	"""Create snapshots of all volumes."""

	for i in instance_manager.get_ec2_instances(project, instance):
		was_running = instance_manager.is_instance_running(i)
		
		if try_stop_instance(i):
			i.wait_until_stopped()
			for v in i.volumes.all():
				if instance_manager.volume_has_pending_snapshot(v):
					print("Skipping {0} volume, snapshot already in progress".format(v.id))
				else:
					print("Creating snapshot of {0} volume...".format(v.id))
					v.create_snapshot(Description="Created by EC2 Snapshot Manager")
			if was_running:
				print("Starting {0} instance...".format(i.id))
				i.start()
				i.wait_until_running()

	return


@cli.group('volumes')
def volumes():
	"""Commands for EC2 volumes."""


@volumes.command('list')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
@click.option('--instance', default=None, help="Specify an instance id")
def list_volumes(project, instance):
	"""List volumes for EC2 instaces"""

	for i in instance_manager.get_ec2_instances(project):
		for v in i.volumes.all():
			print(', '.join([
				v.id,
				i.id,
				v.state,
				str(v.size) + ' GiB',
				v.encrypted and "Encrypted" or "Not Encrypted"
			]))
	return


@cli.group('snapshots')
def snapshots():
	"""Commands for EC2 volumes snapshots."""


@snapshots.command('list')
@click.option('--project', default=None, help="Filter instances based on 'project' tag")
@click.option('--instance', default=None, help="Specify an instance id")
@click.option('--all', 'list_all', default=False, is_flag = True, help="List all snapshots for each volume, default is False")
def list_snapshots(project, instance, list_all):
	"""List snapshots for EC2 instances"""

	for i in instance_manager.get_ec2_instances(project, instance):
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(', '.join([
					s.id,
					v.id,
					i.id,
					s.state,
					s.progress,
					s.start_time.strftime("%x at %X %z")
				]))

				if s.state == constants.COMPLETED_STATE and not list_all:
					break

	return


def try_stop_instance(instance):
	"""Try to stop an EC2 instance."""
	if instance_manager.is_instance_running(instance):
		print("Stopping {0} instance...".format(instance.id))
		instance.stop()
		return True
	elif instance_manager.is_instance_stopped(instance):
		print("{0} instance is already in stopped state...".format(instance.id))
		return True
	else:
		print("Skipping {0} instance in {1} state".format(instance.id, instance.state['Name']))
		return False


if __name__ == '__main__':
	cli(None, None)
