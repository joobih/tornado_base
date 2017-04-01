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

4.增加user到docker用户组中

sudo groupadd docker
sudo gpasswd -a cuijun docker
sudo service docker restart

重启会话
