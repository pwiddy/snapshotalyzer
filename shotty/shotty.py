import boto3
import click
    
session = boto3.Session(profile_name='snapshotalyzer')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
        help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    
    instances = filter_instances(project)

    for i in instances:
        tags = {} 
        # Convert list of dictionaries, to a single dictionary of tags
        if i.tags != None:
            for t in i.tags:
                tags[t['Key']] = t['Value']

        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no project>')
            )))

    return

@instances.command('start')
@click.option('--project', default=None,
        help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)
    
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return


@instances.command('stop')
@click.option('--project', default=None,
        help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)
    
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

if __name__=='__main__':
#    print(sys.argv)
    instances()