Roundcube webmail
=================

Fully configured mail hosting with SMTP and secure IMAP. Be sure to:

 - Add a public key to `./ssl/root_authorized_keys`
 - Save your public key chain to `./ssl/mail.pem`
    - Generate using `cat my.crt intermediate.crt ca.crt >mail.pem`
 - Save your private key to `./ssl/mail.key`
 - Set your hostname in the Dockerfile (roundcube configuration section)

Then build and start the container:

    $ sudo docker build -t=roundcube .
    $ sudo docker run -d -p 8080:80 roundcube
