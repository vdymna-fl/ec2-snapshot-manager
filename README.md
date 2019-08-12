# EC2 Snapshot Manager
Small python CLI to manage AWS EC2 instances, volumes and snapshots using boto3.

## Running (Dev)
The project uses [pipenv](https://docs.pipenv.org/en/latest/) to manage a virtualenv and packages - `pip3 install pipenv`

`pipenv run python -m ec2_manager.ec2_manager [options] <command> <subcommand> [options]`

`pipenv run python -m ec2_manager.ec2_manager --help` for more detailded help info

*--profile* - optional, specify non-default AWS profile name  
*--region* - optional, specify AWS region name  
*commands* - instances, volumes or snapshosts  
*subcommand* - list, start, stop, reboot or snapshot (depends on the command `--help` for more info)  
*--project* - optional, filter list of instances by project tag  
*--instance* - optional, specific instance id

## Distribution package and local install
`pipenv run python setup.py bdist_wheel`  
`pip3 install dist\EC2_Snapshot_Manager-0.1-py3-none-any.whl`  
`ec2-manager --help`  
