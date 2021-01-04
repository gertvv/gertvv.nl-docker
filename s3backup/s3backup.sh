#!/bin/bash
FILENAME="backup-$(date --iso-8601).tar.bz2"
tar cjvf "$FILENAME" /home /var/mail
./s3put.rb "$FILENAME" "$S3_BUCKET"
