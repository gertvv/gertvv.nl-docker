Mail hosting
============

Fully configured mail hosting with authenticated SMTP and secure IMAP. The
server supports:

 - Encrypted IMAP using STARTTLS on port 143 or SSL on port 993. Unencrypted
   connections not allowed.
 - Unencrypted SMTP on port 25 for delivery to local users.
 - Authenticated SMTP on port 25 using STARTTLS for relay.

Be sure to:

 - Save your public key chain to `./ssl/mail.pem`
    - Generate using `cat my.crt intermediate.crt ca.crt >mail.pem`
 - Save your private key to `./ssl/mail.key`
 - Set your mailname in `./mailname`
 - Set the domains for which you accept e-mail in
   `./exim4/update-exim4.conf.conf`
 - Set up users in the following files (to be appended to the corresponding
   files in `/etc`):
    - users/passwd
    - users/shadow
    - users/group
    - users/aliases

You also need to create a container MAILDATA that exposes the volumes `/var/mail` and `/home`.

Then build and start the container:

    $ sudo docker build -t=mail-server .
    $ sudo docker run -d --name mail-server -h "mail.gertvv.nl" -volumes-from MAILDATA -p 25:25 -p 465:465 -p 143:143 -p 993:993 mail-server

Testing
-------

Generate a self-signed certificate for testing:

    $ openssl req -newkey rsa:2048 -nodes -keyout mail.key -x509 -days 365 -out mail.pem

Test local delivery via SMTP:

    $ telnet localhost 25
    < 220 mail.gertvv.nl ESMTP Exim 4.86_2 Ubuntu Tue, 02 Jan 2018 09:41:35 +0000
    > EHLO example.com
    < 250-mail.gertvv.nl Hello example.com [172.17.0.1]
    > MAIL FROM:<test@example.com>
    < 250 OK
    > RCPT TO:<gert@gertvv.nl>
    < 250 Accepted
    > DATA
    < 354 Enter message, ending with "." on a line by itself
    > Subject: testing 123
    > .
    < 250 OK id=1eWJ4w-000020-Rv
    > QUIT
    < 221 mail.gertvv.nl closing connection

Test relay not allowed without authentication:

    > MAIL FROM:<gert@gertvv.nl>
    < 250 OK
    > RCPT TO:<test@example.com>
    < 550 relay not permitted

Test login not allowed without TLS:

    $ telnet localhost 25
    < 220 mail.gertvv.nl ESMTP Exim 4.86_2 Ubuntu Tue, 02 Jan 2018 09:51:40 +0000
    > EHLO mail.gertvv.nl
    < 250-mail.gertvv.nl Hello mail.gertvv.nl [172.17.0.1]
    > AUTH PLAIN
    < 503 AUTH command used when not advertised

Encode credentials for SMTP AUTH PLAIN:

    $ echo -ne "user\0user\0pass" | base64
    dXNlcgB1c2VyAHBhc3M=

Test StartTLS and authentication for SMTP:

    $ echo -ne 'test\0test\01234' | base64
    $ openssl s_client -quiet -connect localhost:25 -starttls smtp
    < 220 mail.gertvv.nl ESMTP Exim 4.86_2 Ubuntu Tue, 02 Jan 2018 14:52:33 +0000
    > EHLO mail.gertvv.nl
    < 250-mail.gertvv.nl Hello mail.gertvv.nl [172.17.0.1]
    > AUTH PLAIN
    < 334
    > [encoded credentials]
    < 235 Authentication succeeded

Test SSL for SMTP:

    $ openssl s_client -quiet -connect localhost:465
    < 220 mail.gertvv.nl ESMTP Exim 4.86_2 Ubuntu Tue, 02 Jan 2018 14:52:33 +0000

Test StartTLS for IMAP:

    $ openssl s_client -quiet -connect localhost:143 -starttls imap
    > a login "user" "pass"
    < a OK [CAPABILITY ...] Logged in
    > b select inbox
    < ...
    < * 1 EXISTS
    < * 1 RECENT
    < ...
    < b OK [READ-WRITE] Select completed (0.000 + 0.000 secs).
    > c fetch 1:1 (BODY[HEADER.FIELDS (Subject)])
    < * 1 FETCH (FLAGS (\Seen \Recent) BODY[HEADER.FIELDS (SUBJECT)] {24}
    < Subject: testing 123
    <
    < )
    < c OK Fetch completed (0.003 + 0.000 + 0.002 secs).


Test SSL for IMAP:

    $ openssl s_client -quiet -connect localhost:993
    > a login "user" "pass"
    < a OK [CAPABILITY ...] Logged in

TODO
----

 - CRON job for SpamAssassin learning (http://help.directadmin.com/item.php?id=188)
