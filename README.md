# awsmfalogin
Speeds up the process of getting an AWS session token into your environment variables

Add your IAM key using the `aws configure` command

run:  
`python3 awsmfalogin.py -u <your aws username> <your mfa token>`

You can also specify your mfa device serial number:
`python3 awsmfalogin.py -s <your aws mfa device serial number> <your mfa token>`

This will print out the commands you need to run to get the new IAM creds into environment variables. Copy-paste them into the terminal, if you are on linux you can execute the output automatically by running as a subcommand:  
`$(python3 awsmfalogin.py -u <your aws username> <your mfa token>)`

You need boto3 installed for this to work. This script will always use the IAM creds in your .aws/credentials file

