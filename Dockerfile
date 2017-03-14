FROM ubuntu

MAINTAINER cui jun "1006536507@qq.com"

COPY ./requirements.txt ~/
COPY ./vimrc ~/

RUN apt-get update ;\
    apt-get install python ;\
    apt-get install vim ;\
    apt-get install python-pip ;\
    pip install -U pip ;\
    cd ~/ ;\
    mkdir src/ ;\
    cd src ;\
    mv ~/requirements.txt ./requirements.txt
    pip install -r requirements.txt
    mv ~/vimrc ~/.vimrc 
    
