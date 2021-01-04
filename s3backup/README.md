Build and run the docker container:

```
docker build . -t mail-backup

docker run --rm --volumes-from MAILDATA \
  -e RSA_KEY_PASSPHRASE=<passphrase> \
  -e S3_BUCKET=<bucket> \
  -e AWS_ACCESS_KEY_ID=<key_id> \
  -e AWS_SECRET_ACCESS_KEY=<secret_key> \
  -e AWS_DEFAULT_REGION=<region> \
  mail-backup
```

Run the put/get scripts from outside their own directory:
```
BUNDLE_GEMFILE=${S3BACKUP}/Gemfile bundle exec ${S3BACKUP}/s3[get|put].rb <objectKey> <bucketName>
```
