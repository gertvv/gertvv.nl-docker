FROM phusion/baseimage:0.10.1

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# Install lighttpd, php, sqlite
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y lighttpd
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y php php-cgi php-mcrypt php-pspell php-xml php-mbstring
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sqlite php-sqlite3

# Install curl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y curl

# Download roundcube
RUN curl -L "https://github.com/roundcube/roundcubemail/releases/download/1.3.7/roundcubemail-1.3.7-complete.tar.gz" | tar xzf -
RUN mv roundcubemail-1.3.7 /var/www/roundcube
RUN mkdir /var/www/roundcube/db
RUN chown www-data.www-data /var/www/roundcube/temp
RUN chown www-data.www-data /var/www/roundcube/logs
RUN chown www-data.www-data /var/www/roundcube/db

## SSL certificates
ADD ssl/mail.key /etc/ssl/private/mail.key
RUN chmod 0400 /etc/ssl/private/mail.key
ADD ssl/mail.pem /etc/ssl/certs/mail.pem
RUN chmod 0444 /etc/ssl/certs/mail.pem

## lighttpd configuration
ADD lighttpd.conf /etc/lighttpd/lighttpd.conf
RUN lighty-enable-mod fastcgi
RUN lighty-enable-mod fastcgi-php
RUN mkdir /var/run/lighttpd
RUN chown www-data.www-data /var/run/lighttpd

## roundcube configuration
RUN cp /var/www/roundcube/config/config.inc.php.sample /var/www/roundcube/config/config.inc.php
RUN sed -i "s|^\(\$config\['default_host'\] =\).*$|\1 'ssl://mail.gertvv.nl';|" /var/www/roundcube/config/config.inc.php
RUN sed -i "s|^\(\$config\['smtp_server'\] =\).*$|\1 'tls://mail.gertvv.nl';|" /var/www/roundcube/config/config.inc.php
RUN sed -i "s|^\(\$config\['db_dsnw'\] =\).*$|\1 'sqlite:////var/www/roundcube/db/sqlite.db?mode=0646';|" /var/www/roundcube/config/config.inc.php
RUN sed -i "s|^\(\$config\['des_key'\] =\).*$|\1 '$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1)';|" /var/www/roundcube/config/config.inc.php

RUN rm -r /var/www/roundcube/installer

## Add runit scripts
RUN mkdir /etc/service/lighttpd
COPY service/lighttpd.sh /etc/service/lighttpd/run
RUN chmod +x /etc/service/lighttpd/run

RUN mkdir /var/log/runit

## Image configuration
EXPOSE 80
CMD ["/sbin/my_init"]
