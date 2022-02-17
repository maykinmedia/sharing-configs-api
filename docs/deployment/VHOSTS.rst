Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess sharing-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/sharing/log/apache2/error.log"
        CustomLog "/srv/sites/sharing/log/apache2/access.log" common

        WSGIProcessGroup sharing-<target>

        Alias /media "/srv/sites/sharing/media/"
        Alias /static "/srv/sites/sharing/static/"

        WSGIScriptAlias / "/srv/sites/sharing/src/sharing/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-sharing-<target>]
    user = <user>
    command = /srv/sites/sharing/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/sharing/src/sharing/wsgi/wsgi_<target>.py
    home = /srv/sites/sharing/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/sharing/log/uwsgi_err.log
    stdout_logfile = /srv/sites/sharing/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_sharing_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/sharing/log/nginx-access.log;
      error_log /srv/sites/sharing/log/nginx-error.log;

      location /500.html {
        root /srv/sites/sharing/src/sharing/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/sharing/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/sharing/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_sharing_<target>;
      }
    }
