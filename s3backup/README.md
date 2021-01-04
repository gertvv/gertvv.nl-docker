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
