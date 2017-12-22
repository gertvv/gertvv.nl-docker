#!/bin/bash
exec /usr/sbin/dovecot -F >>/var/log/runit/dovecot.log 2>&1
