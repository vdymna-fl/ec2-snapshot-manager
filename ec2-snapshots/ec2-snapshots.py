import boto3
import click

PROJECT = 'project' # make this a constant

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

def get_instances_by_project(project):
	instances = []

	if project:
		filters = [{ 'Name': 'tag:'+PROJECT, 'Values': [ project ]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	return instances

@click.group()
def cli():
	"""CLI to manage EC2 snapshots"""

@cli.group('instances')
def instances():
	"Commands for instances"

@instances.command('list')
@click.option('--project', default=None, help="Only instance for project based on tag")
def list_ec2_instaces(project):
	"""List EC2 instances"""
	instances = get_instances_by_project(project)

	for instance in instances:
		tags = { t['Key']: t['Value'] for t in instance.tags or []}

		print(', '.join([ 
			instance.id, 
			instance.instance_type, 
			instance.placement['AvailabilityZone'], 
			instance.state['Name'], 
			instance.public_dns_name,
			tags.get(PROJECT, '<no project>') ]))

	return
        
if __name__ == '__main__':
	cli()