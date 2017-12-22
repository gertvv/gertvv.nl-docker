#!/bin/bash
exec /usr/sbin/spamd --username=spamd --create-prefs --max-children 5 --helper-home-dir >>/var/log/runit/spamd.log 2>&1
