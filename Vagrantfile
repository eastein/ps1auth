# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# Set Environment Variables
export AD_URL="ldap://localhost"
export AD_DOMAIN="VAGRANT"
export AD_BASEDN="CN=Users,DC=vagrant,DC=lan"
export AD_BINDDN="Administrator@VAGRANT"
export AD_BINDDN_PASSWORD="aeng3Oog"
export SECRET_KEY="deesohshoayie6PiGoGaghi6thiecaingai2quab2aoheequ8vahsu1phu8ahJio"
export ZOHO_AUTHTOKEN="add-your-auth-token"
export PAYPAL_RECEIVER_EMAIL="money@vagrant.lan"
export SUPPORT_EMAIL_ADDRESS="vagrant@localhost"
export DISCOURSE_BASE_URL="http://discourse.vagrant.lan"
export DISCOURSE_SSO_SECRET="989175d0b666378b038b344a587033d94334badeb5201321fc05b8e952bc4a8f"

# Update the System
pacman -Syy
pacman -S archlinux-keyring --noconfirm --needed
pacman -S pacman --noconfirm --needed
pacman-db-upgrade
pacman -Su --noconfirm

# Set Timezone
timedatectl set-timezone America/Chicago

# Setup locale.gen
cat << EOF > /etc/locale.gen
en_US.UTF-8 UTF-8
en_US ISO-8859-1
EOF
locale-gen

# Install Dependencies
pacman -S --noconfirm --needed postgresql samba nginx redis python git

# Setup Samba
samba-tool domain provision --realm=vagrant.lan --domain=${AD_DOMAIN} --server-role=dc --use-rfc2307 --adminpass=${AD_BINDDN_PASSWORD}
systemctl start samba
systemctl enable samba

# Set Shell Environment Variables
cat << EOF > .bashrc
export AD_URL=${AD_URL}
export AD_DOMAIN=${AD_DOMAIN}
export AD_BASEDN=${AD_BASEDN}
export AD_BINDDN=${AD_BINDDN}
export AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}
export SECRET_KEY=${SECRET_KEY}
export ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}
export PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}
export SUPPORT_EMAIL_ADDRESS=${SUPPORT_EMAIL_ADDRESS}
export DISCOURSE_BASE_URL=${DISCOURSE_BASE_URL}
export DISCOURSE_SSO_SECRET=${DISCOURSE_SSO_SECRET}
source venv/bin/activate
EOF

#  Setup Database
chmod 755 /home/vagrant
sudo -u postgres initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'
systemctl start postgresql
systemctl enable postgresql
sudo -u postgres createuser --superuser vagrant
sudo -u vagrant createdb ps1auth

# Bootstrap App

sudo -u vagrant python -m venv venv
sudo -u vagrant venv/bin/pip install --find-links=file:///vagrant/wheelhouse --upgrade pip
sudo -u vagrant venv/bin/pip install --find-links=file:///vagrant/wheelhouse wheel
sudo -u vagrant venv/bin/pip install --find-links=file:///vagrant/wheelhouse -r /vagrant/requirements/local.txt
sudo -u vagrant venv/bin/pip install gunicorn
sudo -u vagrant -E venv/bin/python /vagrant/manage.py migrate --noinput
# Load Fixture data
sudo -u vagrant -E venv/bin/python /vagrant/manage.py loaddata doors

# Setup systemd environment file
cat << EOF > /home/vagrant/ps1auth.conf
AD_URL=${AD_URL}
AD_DOMAIN=${AD_DOMAIN}
AD_BASEDN=${AD_BASEDN}
AD_BINDDN=${AD_BINDDN}
AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}
SECRET_KEY=${SECRET_KEY}
ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}
PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}
SUPPORT_EMAIL_ADDRESS=${SUPPORT_EMAIL_ADDRESS}
DISCOURSE_BASE_URL=${DISCOURSE_BASE_URL}
DISCOURSE_SSO_SECRET=${DISCOURSE_SSO_SECRET}
EOF

# PS1Auth Systemd Service File
cat << EOF > /etc/systemd/system/ps1auth.service
[Unit]
Description=PS1 Auth (Member's site)
After=vboxservice.service

[Service]
Type=simple
User=vagrant
WorkingDirectory=/vagrant
ExecStart=/home/vagrant/venv/bin/gunicorn --log-level debug ps1auth.wsgi:application --reload
EnvironmentFile=-/home/vagrant/ps1auth.conf

[Install]
WantedBy=multi-user.target
EOF

# PS1Auth systemd socket file
cat << EOF > /etc/systemd/system/ps1auth.socket
[Socket]
ListenStream=/tmp/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Nginx config
cat << EOF > /etc/nginx/nginx.conf
error_log /var/log/nginx/error.log;
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        off;
    keepalive_timeout  65;
    access_log /var/log/nginx/access.log combined;
    upstream ps1auth
    {
        server unix:/tmp/gunicorn.sock fail_timeout=0;
    }
    server {
        listen       8001;
        server_name  _;
        client_max_body_size 4G;
        keepalive_timeout 5;
        root /vagrant;
        location / {
            proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
            proxy_set_header Host \\$http_host;
            proxy_redirect off;
            proxy_pass   http://ps1auth;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
EOF

# PS1Auth Celery Worker Systemd Service File
cat << EOF > /etc/systemd/system/celery.service
[Unit]
Description=PS1 Auth Celery Worker
After=vboxservice.service

[Service]
Type=simple
User=vagrant
WorkingDirectory=/vagrant
ExecStart=/home/vagrant/venv/bin/celery -A ps1auth worker -l info
EnvironmentFile=-/home/vagrant/ps1auth.conf
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure App to Start Automatically
systemctl start ps1auth.socket
systemctl enable ps1auth.socket
systemctl start nginx
systemctl enable nginx
systemctl start redis
systemctl enable redis
systemctl start celery
systemctl enable celery
systemctl start systemd-journal-gatewayd.socket
systemctl enable systemd-journal-gatewayd.socket

SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hef/arch"
  config.vm.provision "shell", inline: $script
  config.vm.network "forwarded_port", guest: 5555, host: 5555, auto_correct: true
  config.vm.network "forwarded_port", guest: 8001, host: 8001, auto_correct: true
  config.vm.network "forwarded_port", guest: 19531, host: 8002, auto_correct: true
  config.vm.network "forwarded_port", guest: 389, host: 1389, auto_correct: true
  config.vm.provider :libvirt do |_, override|
    override.vm.synced_folder ".", "/vagrant", type: "9p", accessmode: "squash"
  end
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end
end
