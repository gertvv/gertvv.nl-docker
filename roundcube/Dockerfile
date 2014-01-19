FROM ubuntu:12.04

# Add universe for supervisor and lighttpd
RUN sed -i.bak 's/main$/main universe/' /etc/apt/sources.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# Install supervisor, openssh
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y supervisor
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server 

# Install lighttpd, php, sqlite
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y lighttpd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y php5 php5-cgi php5-mcrypt php5-pspell
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sqlite php5-sqlite

# Install curl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y curl

# Download roundcube
RUN curl -L "http://sourceforge.net/projects/roundcubemail/files/roundcubemail/0.9.5/roundcubemail-0.9.5.tar.gz/download" | tar xzf -
RUN mv roundcubemail-0.9.5 /var/www/roundcube
RUN mkdir /var/www/roundcube/db
RUN chown www-data.www-data /var/www/roundcube/temp
RUN chown www-data.www-data /var/www/roundcube/logs
RUN chown www-data.www-data /var/www/roundcube/db

## enable root login using a certificate
RUN mkdir -p /var/run/sshd
RUN mkdir /root/.ssh
ADD ssl/root_authorized_keys /root/.ssh/authorized_keys
RUN chown root.root /root/.ssh/authorized_keys

## SSL certificates
ADD ssl/mail.key /etc/ssl/private/mail.key
RUN chmod 0400 /etc/ssl/private/mail.key
ADD ssl/mail.pem /etc/ssl/certs/mail.pem
RUN chmod 0444 /etc/ssl/certs/mail.pem

## supervisor configuration
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

## lighttpd configuration
ADD lighttpd.conf /etc/lighttpd/lighttpd.conf
RUN lighttpd-enable-mod fastcgi fastcgi-php

## roundcube configuration
RUN cp /var/www/roundcube/config/db.inc.php.dist /var/www/roundcube/config/db.inc.php
RUN cp /var/www/roundcube/config/main.inc.php.dist /var/www/roundcube/config/main.inc.php
RUN sed -i "s|^\(\$rcmail_config\['default_host'\] =\).*$|\1 'ssl://mail.gertvv.nl';|" /var/www/roundcube/config/main.inc.php
RUN sed -i "s|^\(\$rcmail_config\['mail_domain'\] =\).*$|\1 'gertvv.nl';|" /var/www/roundcube/config/main.inc.php
RUN sed -i "s|^\(\$rcmail_config\['smtp_server'\] =\).*$|\1 'mail.gertvv.nl';|" /var/www/roundcube/config/main.inc.php
RUN sed -i "s|^\(\$rcmail_config\['smtp_user'\] =\).*$|\1 '%u';|" /var/www/roundcube/config/main.inc.php
RUN sed -i "s|^\(\$rcmail_config\['smtp_pass'\] =\).*$|\1 '%p';|" /var/www/roundcube/config/main.inc.php
RUN sed -i "s|^\(\$rcmail_config\['db_dsnw'\] =\).*$|\1 'sqlite:////var/www/roundcube/db/sqlite.db?mode=0646';|" /var/www/roundcube/config/db.inc.php

RUN rm -r /var/www/roundcube/installer

# http
EXPOSE 80

CMD ["/usr/bin/supervisord"]
