#!/bin/bash
exec /sbin/setuser Debian-exim /usr/sbin/exim4 -bdf -q30m -oX 465:25 >>/var/log/runit/exim4.log 2>&1
