Mail hosting
============

Fully configured mail hosting with SMTP and secure IMAP. Be sure to:

 - Add a public key to `./ssl/root_authorized_keys`
 - Save your public key chain to `./ssl/mail.pem`
    - Generate using `cat my.crt intermediate.crt ca.crt >mail.pem`
 - Save your private key to `./ssl/mail.key`
 - Set your mailname in `./mailname`
 - Set the domains for which you accept e-mail in
   `./exim4/update-exim4.conf.conf`

Then build and start the container:

    $ sudo docker build -t=mail-server .
    $ sudo docker run -d -p 2222:22 -p 25:25 -p 143:143 -p 993:993 mail-server

To add users and aliases, login using SSH:

    $ ssh -p 2222 root@localhost
    # adduser gert
    ...
    # echo 'root: gert' >> /etc/aliases

TODO
----

 - Allow relay for authenticated SMTP users & enable StartTLS (https://wiki.debian.org/Exim)
 - CRON job for SpamAssassin learning (http://help.directadmin.com/item.php?id=188)
