"""Classes to interact with EC2 resources."""

from ec2_manager import constants


class InstanceManager:
    """Manager for interactions with EC2 instances."""


    def __init__(self, session):
        self.session = session
        self.ec2 = self.session.resource('ec2')


    def get_ec2_instances(self, project_tag, instance_id=None):
        """Get list of EC2 instances and optionally filter by project name"""
        instances = []

        if instance_id:
            instances = self.ec2.instances.filter(InstanceIds=[instance_id])
        elif project_tag:
            filters = [{'Name': 'tag:' + constants.PROJECT_TAG, 'Values': [project_tag]}]
            instances = self.ec2.instances.filter(Filters=filters)
        else:
            instances = self.ec2.instances.all()

        return instances


    @staticmethod
    def is_instance_running(instance):
        """Check if instance is in running state"""
        return instance.state['Name'] == constants.RUNNING_STATE
    

    @staticmethod
    def is_instance_stopped(instance):
        """Check if instance is in stopped state"""
        return instance.state['Name'] == constants.STOPPED_STATE


    @staticmethod
    def volume_has_pending_snapshot(volume):
        """Check if volume has a pending snapshot"""
        snapshots = list(volume.snapshots.all())
        return snapshots and snapshots[0].state == constants.PENDING_STATE
