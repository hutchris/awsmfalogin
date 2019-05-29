# awsmfalogin
Speeds up the process of getting an AWS session token into your environment variables

Add your IAM key using the `aws configure` command

run: `python3 awsmfalogin.py -s <your mfa serial number> <your mfa token>`

This will print out the commands you need to run to get the new IAM creds into environment variables. Copy-paste them into the terminal, if you are on linux you can execute the output automatically by running as a subcommand: `$(python3 awsmfalogin.py -s <your mfa serial number> <your mfa token>)`

You need boto3 installed for this to work. This script will always use the IAM creds in your .aws/credentials file

You can prevent the need to type in your serial number every time by storing it as a default in the argparse argument. Change this:
`parser.add_argument('--serialnumber','-s',help='serial number from mfa token, found in your IAM user profile in the AWS console')`
To this:
`parser.add_argument('--serialnumber','-s',help='serial number from mfa token, found in your IAM user profile in the AWS console',default='arn:aws:iam::0123012301230123:mfa/example')`
