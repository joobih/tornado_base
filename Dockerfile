FROM fedeg/python-vim

MAINTAINER cui jun "1006536507@qq.com"

COPY ./requirements.txt ~/

RUN apt-get install python ;\
    apt-get install python-pip ;\
    pip install -U pip ;\
    cd ~/ ;\
    mkdir src/ ;\
    cd src ;\
    mv ~/requirements.txt ./requirements.txt
    pip install -r requirements.txt
    
