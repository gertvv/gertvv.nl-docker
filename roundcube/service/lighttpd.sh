#!/bin/bash
exec /usr/sbin/lighttpd -D -f /etc/lighttpd/lighttpd.conf >>/var/log/runit/lighttpd.log 2>&1
