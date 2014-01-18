# Fully configured mail server with SMTP, IMAP and SpamAssassin
#
#  - use the sshd to add users and edit /etc/aliases

FROM ubuntu:12.04

# Add universe for supervisor
RUN sed -i.bak 's/main$/main universe/' /etc/apt/sources.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y exim4-daemon-heavy
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dovecot-imapd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y spamassassin
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y supervisor
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sa-exim

## enable root login using a certificate
RUN mkdir -p /var/run/sshd
RUN mkdir /root/.ssh
ADD ssl/root_authorized_keys /root/.ssh/authorized_keys
RUN chown root.root /root/.ssh/authorized_keys

## exim4 configuration
ADD mailname /etc/mailname
ADD exim4 /etc/exim4
RUN sed -i '1ilocal_scan_path = /usr/lib/exim4/local_scan/sa-exim.so\n' /etc/exim4/exim4.conf.template
RUN sed -i 's/^SAEximRunCond: 0$/#SAEximRunCond: 0/' /etc/exim4/sa-exim.conf
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
RUN chmod 0400 /etc/ssl/private/mail.key
ADD ssl/mail.pem /etc/ssl/certs/mail.pem
RUN chmod 0444 /etc/ssl/certs/mail.pem

## supervisor configuration
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ssh, smtp, imap, imaps
EXPOSE 22 25 143 993

CMD ["/usr/bin/supervisord"]
