# Fully configured mail server with SMTP, IMAP and SpamAssassin
#
#  - use the sshd to add users and edit /etc/aliases

FROM ubuntu:12.04

# Add universe for supervisor
RUN sed -i.bak 's/main$/main universe/' /etc/apt/sources.list
RUN apt-mark hold initscripts udev plymouth mountall
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y supervisor
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y exim4-daemon-heavy spamassassin sa-exim
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dovecot-imapd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sasl2-bin

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y procmail

## enable root login using a certificate
RUN mkdir -p /var/run/sshd
RUN mkdir /root/.ssh
ADD ssl/root_authorized_keys /root/.ssh/authorized_keys
RUN chown root.root /root/.ssh/authorized_keys

## exim4 configuration
ADD mailname /etc/mailname
ADD exim4 /etc/exim4
# Enable spamassassin
RUN sed -i '1ilocal_scan_path = /usr/lib/exim4/local_scan/sa-exim.so\n' /etc/exim4/exim4.conf.template
RUN sed -i 's/^SAEximRunCond: 0$/#SAEximRunCond: 0/' /etc/exim4/sa-exim.conf
# Enable TLS
RUN sed -i '1iMAIN_TLS_ENABLE = yes\nMAIN_TLS_PRIVATEKEY = /etc/exim4/mail.key\nMAIN_TLS_CERTIFICATE = /etc/exim4/mail.pem\n' /etc/exim4/exim4.conf.template
RUN usermod -a -G ssl-cert Debian-exim
# Enable port 465
RUN sed -i 's/SMTPLISTENEROPTIONS=.*/SMTPLISTENEROPTIONS='"'"'-oX 465:25'"'"'/' /etc/default/exim4
RUN sed -i '/\.ifdef MAIN_TLS_ENABLE/atls_on_connect_ports=465' /etc/exim4/exim4.conf.template
# Enable authentication
RUN echo 'plain_saslauthd_server:\n  driver = plaintext\n  public_name = PLAIN\n  server_condition = ${if saslauthd{{$auth2}{$auth3}}{1}{0}}\n  server_set_id = $auth2\n  server_prompts = :\n  .ifndef AUTH_SERVER_ALLOW_NOTLS_PASSWORDS\n  server_advertise_condition = ${if eq{$tls_cipher}{}{}{*}}\n  .endif' >>/etc/exim4/exim4.conf.template
RUN usermod -a -G sasl Debian-exim
RUN update-exim4.conf

## Dovecot configuration
# use mbox format
RUN sed -i 's/^#mail_access_groups =.*/mail_access_groups = mail/' /etc/dovecot/conf.d/10-mail.conf
RUN sed -i 's/^#mail_location =.*/mail_location = mbox:~\/mail:INBOX=\/var\/mail\/%u/' /etc/dovecot/conf.d/10-mail.conf
# require SSL for all connections
RUN sed -i 's/^#ssl =.*/ssl = required/' /etc/dovecot/conf.d/10-ssl.conf
RUN sed -i 's/^ssl_cert =.*/ssl_cert = <\/etc\/ssl\/certs\/mail.pem/' /etc/dovecot/conf.d/10-ssl.conf
RUN sed -i 's/^ssl_key =.*/ssl_key = <\/etc\/ssl\/private\/mail.key/' /etc/dovecot/conf.d/10-ssl.conf
RUN sed -i 's/^#log_path =.*/log_path = \/dev\/stderr/' /etc/dovecot/conf.d/10-logging.conf

## SSL certificates
ADD ssl/mail.key /etc/ssl/private/mail.key
RUN chmod 0440 /etc/ssl/private/mail.key
ADD ssl/mail.pem /etc/ssl/certs/mail.pem
RUN chmod 0444 /etc/ssl/certs/mail.pem
RUN chown root.ssl-cert /etc/ssl/private/mail.key /etc/ssl/certs/mail.pem

# For some reason Exim refuses to read the certificates from /etc/ssl
RUN cp /etc/ssl/private/mail.key /etc/exim4/
RUN cp /etc/ssl/certs/mail.pem /etc/exim4/
RUN chgrp ssl-cert /etc/exim4/mail.key /etc/exim4/mail.pem

## supervisor configuration
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ssh, smtp, smtps, imap, imaps
EXPOSE 22 25 465 143 993

CMD ["/usr/bin/supervisord"]
