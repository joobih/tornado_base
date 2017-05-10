#!/bin bash

sudo apt-get update

#安装mono
#这个程序可以用来模拟运行windows环境的程序

sudo apt-get install mono-complete
#下载好Fiddler for Mono版本
#mono Fiddler.exe

#安装vim
sudo cp vim74_new.tar.gz /opt
sudo cd /opt
sudo tar -zxvf vim74_new.tar.gz
sudo cd vim74
sudo ./configure
sudo make
sudo make install

cp -r vim/ ~/
cp vimrc ~/.vimrc

#安装python库等
sudo apt-get install python=2.7.12
sudo apt-get install python-pip
sudo pip install -U pip
sudo pip install tornado
sudo pip install thrift-compiler
sudo pip install pika
sudo pip install bs4
sudo pip install pymongo

#安装pyhs2
sudo apt-get install libsasl2-dev
sudo apt-get install libsasl2-modules-gssapi-mit
sudo pip install pyhs2

#安装scrapy
sudo apt-get install libxml2-dev libxslt1-dev
sudo pip install scrapy


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

