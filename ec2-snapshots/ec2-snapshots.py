import boto3
import click

PROJECT = 'project' # make this a constant

session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

@click.command()
@click.option('--project', default=None, help="Only instance for project (tag project:<name>)")
def list_ec2_instaces(project):
	"""List EC2 instances."""
	instances = []

	if project:
		filters = [{ 'Name': 'tag:'+PROJECT, 'Values': [ project ]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

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
	list_ec2_instaces(None)