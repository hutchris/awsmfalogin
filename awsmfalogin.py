#!/usr/bin/env python3

import os
import subprocess
import platform
import boto3
import argparse

parser = argparse.ArgumentParser(
    description='Speeds up the process of getting an AWS session token into your environment variables',
    epilog='You must enter either --username/-u or --serialnumber/-s'
    )
parser.add_argument('token',help='Value from the authenticator token on your phone')
parser.add_argument('--username','-u',help='AWS username')
parser.add_argument('--serialnumber','-s',help='serial number from mfa token, found in your IAM user profile in the AWS console')
parser.add_argument('--profile','-p',help='Credential profile from your ~/.aws/credentials file. Default=default',default='default')
args = parser.parse_args()

if args.serialnumber is None and args.username is None:
    raise(Error("Either username or serialnumber must be specified"))

session = boto3.Session(profile_name=args.profile)

if args.serialnumber is None:
    iam = session.client('iam')
    mfaDevices = iam.list_virtual_mfa_devices()
    for device in mfaDevices['VirtualMFADevices']:
        if 'User' in device:
            if 'UserName' in device['User'] and device['User']['UserName'] == args.username:
                    serialnumber = device['SerialNumber']
else:
    serialnumber = args.serialnumber

sts = session.client('sts')
creds = sts.get_session_token(SerialNumber=serialnumber,TokenCode=args.token)

# ak = 'AWS_ACCESS_KEY_ID={}'.format(creds['Credentials']['AccessKeyId'])
# sk = 'AWS_SECRET_ACCESS_KEY={}'.format(creds['Credentials']['SecretAccessKey'])
# tk = 'AWS_SESSION_TOKEN={}'.format(creds['Credentials']['SessionToken'])
# rg = 'AWS_DEFAULT_REGION={}'.format(session.region_name)


ak = creds['Credentials']['AccessKeyId']
sk = creds['Credentials']['SecretAccessKey']
tk = creds['Credentials']['SessionToken']
rg = session.region_name

if platform.system() == 'Linux':
    print(f'export AWS_ACCESS_KEY_ID={ak} AWS_SECRET_ACCESS_KEY={sk} AWS_SESSION_TOKEN={tk} AWS_DEFAULT_REGION={rg}')
else:
    pid = os.getppid()
    parent_name = subprocess.check_output(['wmic', 'process', 'where', f'ProcessId={pid}', 'get', 'Name'], text=True).strip().split()[-1]
    if "powershell" in parent_name.lower():
        print(f'$Env:AWS_ACCESS_KEY_ID="{ak}"')
        print(f'$Env:AWS_SECRET_ACCESS_KEY="{sk}"')
        print(f'$Env:AWS_SESSION_TOKEN="{tk}"')
        print(f'$Env:AWS_DEFAULT_REGION="{rg}"')
    else:
        print(f'set AWS_ACCESS_KEY_ID={ak}')
        print(f'set AWS_SECRET_ACCESS_KEY={sk}')
        print(f'set AWS_SESSION_TOKEN={tk}')
        print(f'set AWS_DEFAULT_REGION={rg}')
