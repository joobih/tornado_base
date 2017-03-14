# tornado_base
基本的tornadobase类

1.安装docker

sudo apt-get install docker.io

2.增加配置文件 /etc/docker/daemon.json

    {                                                                                           
      registry-mirrors:["https://2iu94llq.mirror.aliyuncs.com","http://18ec2e74.m.daocloud.io"]                                                                        
    }

3.重启docker服务

service docker restart
