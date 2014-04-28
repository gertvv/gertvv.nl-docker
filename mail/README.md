Mail hosting
============

Fully configured mail hosting with authenticated SMTP and secure IMAP. The
server supports:

 - Encrypted IMAP using STARTTLS on port 143 or SSL on port 993. Unencrypted
   connections not allowed.
 - Unencrypted SMTP on port 25 for delivery to local users.
 - Authenticated SMTP on port 25 using STARTTLS for relay.
 - SSH login to create additional users an aliases.

Be sure to:

 - Add a public key to `./ssl/root_authorized_keys`
 - Save your public key chain to `./ssl/mail.pem`
    - Generate using `cat my.crt intermediate.crt ca.crt >mail.pem`
 - Save your private key to `./ssl/mail.key`
 - Set your mailname in `./mailname`
 - Set the domains for which you accept e-mail in
   `./exim4/update-exim4.conf.conf`

You also need to create a container MAILDATA that exposes the volumes `/var/mail` and `/home`.

Then build and start the container:

    $ sudo docker build -t=mail-server .
    $ sudo docker run -d -name mail-server -h "mail.gertvv.nl" -volumes-from MAILDATA -p 2222:22 -p 25:25 -p 465:465 -p 143:143 -p 993:993 mail-server

To add users and aliases, login using SSH:

    $ ssh -p 2222 root@localhost
    # adduser gert
    ...
    # echo 'root: gert' >> /etc/aliases

TODO
----

 - CRON job for SpamAssassin learning (http://help.directadmin.com/item.php?id=188)
