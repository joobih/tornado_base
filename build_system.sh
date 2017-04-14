#!/bin bash

sudo apt-get update

#安装vim
sudo apt-get install vim
cp -r vim/ ~/
cp vimrc ~/.vimrc

#安装python库等
sudo apt-get install python=2.7.12
sudo apt-get install python-pip
sudo pip install -U pip
sudo pip install tornado
sudo pip install thrift
sudo pip install pika
sudo pip install bs4
sudo pip install pymongo

#安装pyhs2
sudo apt-get install libsasl2-dev
sudo apt-get install libsasl2-modules-gssapi-mit
sudo pip install pyhs2


#安装docker
sudo apt-get install docker.io
sudo cp ./daemon.json /etc/docker/daemon.json
sudo groupadd docker
sudo gpasswd -a cuijun docker
sudo service docker restart

#安装rabbitmq
sudo apt-get install rabbitmq-server

#安装mysql
sudo apt-get install mysql-server mysql-client

#安装redis
sudo apt-get install redis-server

