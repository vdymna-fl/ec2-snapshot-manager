# EC2 Snapshot Manager
Small python CLI to manage AWS EC2 instance snapshots using boto3.

## Running
The project uses [pipenv](https://docs.pipenv.org/en/latest/) to manage a virtualenv and packages - `pip3 install pipenv`

`pipenv run python ec2_manager\ec2_manager.py <command> <subcommand> --<option> [OPTION-VALUE]`

`pipenv run python ec2_manager\ec2_manager.py --help` for more detailded help info

*commands* - instances, volumes or snapshosts  
*subcommand* - list, start, stop, reboot or snapshot (depends on the command `--help` for more info)  
*profile* - optional, specify non-default AWS profile  
*project* - optional, filter list of instances by project tag
*instance* - optional, specific instance id

## Create distribution package
`pipenv run python setup.py bdist_wheel`
