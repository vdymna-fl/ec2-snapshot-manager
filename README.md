# EC2 Snapshot Manager
Small python CLI to manage AWS EC2 instance snapshots using boto3.

## Running
`pipenv run python ec2_manager\ec2_manager.py --profile <AWS PROFILE> <command> <subcommand> --project <PROJECT TAG NAME>`

`pipenv run python ec2_manager\ec2_manager.py --help` for more detailded help info

*commands* - instances, volumes or snapshosts  
*subcommand* - list, start, stop, reboot or snapshot (depends on command `--help` for more info)  
*profile* - optional, specify other non-default profile  
*project* - optional  

## Create distribution package
`pipenv run python setup.py bdist_wheel`
