#!/usr/bin/env bash

mkdir -p /var/tmp/beki/tex
cp tex/logo.png /var/tmp/beki/tex/logo.png
cp tex/template.tex /var/tmp/beki/tex/template.tex
chown -R uwsgi:uwsgi /var/tmp/beki/tex

if [ ! -d /mnt/beki/uwsgi_logs ]
then
    mkdir /mnt/beki/uwsgi_logs
    chown -R uwsgi:uwsgi /mnt/beki/uwsgi_logs
fi

chown -R uwsgi:uwsgi /mnt/beki/uploads
chown uwsgi:uwsgi /mnt/beki/beki.db

service nginx start
uwsgi --ini uwsgi.ini
