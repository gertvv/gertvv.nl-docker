#!/bin/bash
exec /usr/sbin/saslauthd -a pam -d >>/var/log/runit/saslauthd.log 2>&1
