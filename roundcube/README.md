Roundcube webmail
=================

Roundcube webmail hosted using lighttpd and sqlite. Assumes SSL termination is
done via a reverse proxy or load balancer.

Set the mail server's hostname in the Dockerfile (roundcube configuration
section).

Then build and start the container:

    $ docker build . -t roundcube
    $ sudo docker run -d --name roundcube -p 8080:80 roundcube

Optionally, use a volume for `/var/www/roundcube/db`.
