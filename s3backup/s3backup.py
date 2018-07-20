#!/usr/bin/python
import sys
import boto3
from subprocess import call
from datetime import date
import os

fileName = "backup-" + date.today().isoformat() + ".tar.bz2"

# make a compressed backup
call(["tar", "cjvf", fileName, "/home", "/var/mail"])

# encrypt the backup using a passphrase
call(["gpg", "--symmetric", "--batch", "--passphrase", os.environ['ENCRYPTION_PASSPHRASE'], fileName])

# upload to S3
s3 = boto3.resource('s3')
with open(fileName + '.gpg', 'rb') as f:
    object = s3.Bucket(os.environ['S3_BUCKET']).put_object(Key=fileName + '.gpg', Body=f)
