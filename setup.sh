#!/usr/bin/env bash
apt-get update
apt-get install -y libmysqlclient-dev \
                libjpeg-dev \
                zlib1g-dev \
                libpng12-dev \
                python-pip \
                python-dev \
                fonts-noto-cjk \
                libsasl2-dev \
                freetds-dev \
                pkg-config \
                libfreetype6-dev \
                libxml2-dev \
                libxslt-dev \
                lib32z1-dev \
                python-tk 

echo "installing python package"
pip install -r requirements.txt

echo "installing node"
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs
