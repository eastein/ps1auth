Develop inside of Vagrant
=========================

Getting Started with Vagrant
----------------------------

::

    vagrant up

Creating a user
---------------

::

    vagrant ssh
    cd /vagrant
    ./manage.py create_person

Viewing the site
----------------

open a browser to http://127.0.0.1:8001 on the host machine


Development Tips
================

Journald
--------

systemd-journald logs are available at http://127.0.0.1:8002.  Check for ps1auth.service and press the "Jump to End" button.  Trying to scoll past the log window does some strange things, so use the borders around it when going to the bottom of the page.

Restarting the service
----------------------

If you crash the app hard enough, use this command to try and restart
::

    sudo systemctl stop ps1auth && sudo systemctl restart ps1auth.socket

Email
-----

Emails sent from the development site can be found in :file:`cache/mail`


Faster Development iteration
============================

vagrant-cachier
---------------

If you find yourself re-provisioning the vagrant box frequently,
::

    vagrant plugin install vagrant-cachier

This will cause pacman to use a shared nfs path for /var/cache/pacman/pkg

Wheelhouse
----------

One of the slower parts of running `vagrant up` is when pip installs the python package requirements.  This can be made faster by storing off wheel files between runs.
::

    pip wheel --wheel-dir=/vagrant/wheelhouse pip wheel -r /vagrant/requirements/local.txt
