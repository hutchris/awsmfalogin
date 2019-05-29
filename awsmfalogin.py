import os
import platform
import boto3
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('token',help='Value from the authenticator token on your phone')
parser.add_argument('--serialnumber','-s',help='serial number from mfa token, found in your IAM user profile in the AWS console')
args = parser.parse_args()

session = boto3.Session(profile_name='default')
sts = session.client('sts')
creds = sts.get_session_token(SerialNumber=args.serialnumber,TokenCode=args.token)

ak = 'AWS_ACCESS_KEY_ID={}'.format(creds['Credentials']['AccessKeyId'])
sk = 'AWS_SECRET_ACCESS_KEY={}'.format(creds['Credentials']['SecretAccessKey'])
tk = 'AWS_SESSION_TOKEN={}'.format(creds['Credentials']['SessionToken'])

if platform.system() == 'Linux':
    print('export ' + ak + ' ' + sk + ' ' + tk)
else:
    print('set ' + ak)
    print('set ' + sk)
    print('set ' + tk)