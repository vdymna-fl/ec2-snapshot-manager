import boto3
import click

TAG_PROJECT = 'project' # make this a constant
STOPPED_STATE = 'stopped'
RUNNING_STATE = 'running'

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

def get_ec2_instances(project):
	instances = []

	if project:
		filters = [{ 'Name': 'tag:' + TAG_PROJECT, 'Values': [ project ]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	return instances

@click.group()
def cli():
	"""CLI to manage EC2 snapshots"""

@cli.group('instances')
def instances():
	"""Commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instance for project based on tag")
def list_instances(project):
	"""List EC2 instances"""
	
	for i in get_ec2_instances(project):
		tags = { t['Key']: t['Value'] for t in i.tags or []}

		print(', '.join([ 
			i.id, 
			i.instance_type, 
			i.placement['AvailabilityZone'], 
			i.state['Name'], 
			i.public_dns_name or '<no public dns name>',
			tags.get(TAG_PROJECT, '<no project>') 
		]))

	return

@instances.command('start')
@click.option('--project', default=None, help="Only instance for project based on tag")
def start_instances(project):
	"""Start EC2 instances"""

	for i in get_ec2_instances(project):
		if i.state['Name'] == STOPPED_STATE:
			print("Starting {0} instance...".format(i.id))
			i.start()
		else:
			print("Skipping {0} instance in {1} state".format(i.id, i.state['Name']))

@instances.command('stop')
@click.option('--project', default=None, help="Only instance for project based on tag")
def stop_instances(project):
	"""Stop EC2 instances"""

	for i in get_ec2_instances(project):
		if i.state['Name'] == RUNNING_STATE:
			print("Stopping {0} instance...".format(i.id))
			i.stop()
		else:
			print("Skipping {0} instance in {1} state".format(i.id, i.state['Name']))


@cli.group('volumes')
def volumes():
	"""Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, help='Only instance for project based on tag')
def list_volumes(project):
	"""List volumes for EC2 instaces"""

	for i in get_ec2_instances(project):
		for v in i.volumes.all():
			print(', '.join([
				v.id,
				i.id,
				v.state,
				str(v.size) + ' GiB',
				v.encrypted and "Encrypted" or "Not Encrypted"
			]))
	return
      
if __name__ == '__main__':
	cli()