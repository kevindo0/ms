### Docker Install
#### [Centos](https://docs.docker.com/install/linux/docker-ce/centos)
```bash
yum install -y yum-utils device-mapper-persistent-data lvm2
# 设置Docker的存储库
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce
systemctl daemon-reload && systemctl start docker
docker version
```

### Ubuntu Tools
```
apt-get install -y tree
```
### Build basic images
```
# docker/basic
docker build -t ubuntu:16b .
# docker/python3
docker build -t ubuntu:16bp .
```

### save image
```
docker save -o redis.tar ubuntu:redis
docker load -i redis.tar
```

### build redis image
start redis container with password "baobao"
```bash
docker build -t ubuntu:redis .
docker run -d -ti --name redis -p 6379:6379 ubuntu:redis --requirepass baobao
```

### build mongodb image
```bash
docker build -t ubuntu:mongo .
docker run -d -ti --name mongo -p 27017:27017 ubuntu:mongo
```

### build rabbitmq image
```bash
docker build -t rabbit:3.7 .
docker run -d -ti --name rabbit -p 5672:5672 rabbit:3.7
rabbitmqctl add_user rabbit 123456
rabbitmqctl set_permissions rabbit '.*' '.*' '.*'
rabbitmqctl list_user_permissions rabbit
rabbitmqctl list_users
```

### Features
对于使用 systemd 的系统，请在 /etc/docker/daemon.json 中写入如下内容（如果文件不存在请新建该文件）
```
{
  "registry-mirrors": [
    "https://registry.docker-cn.com"
  ]
}
```
之后重新启动服务。
```
$ sudo systemctl restart docker
```

### CMD和ENTRYPOINT指令差异对比:
差异1：CMD指令指定的容器启动时命令可以被docker run指定的命令覆盖，而ENTRYPOINT指令指定的命令不能被覆盖，而是将docker run指定的参数当做ENTRYPOINT指定命令的参数。
差异2：CMD指令可以为ENTRYPOINT指令设置默认参数，而且可以被docker run指定的参数覆盖；
注意:
1、CMD指令为ENTRYPOINT指令提供默认参数是基于镜像层次结构生效的，而不是基于是否在同个Dockerfile文件中。意思就是说，如果Dockerfile指定基础镜像中是ENTRYPOINT指定的启动命令，则该Dockerfile中的CMD依然是为基础镜像中的ENTRYPOINT设置默认参数。

2. CMD command param1 param2 (shell form)
  * shell form，即没有中括号的形式。那么命令command默认是在“/bin/sh -c”下执行的。

3. CMD ["executable","param1","param2"] => (exec form, this is the preferred form)
  * 运行一个可执行的文件并提供参数。

###  Arg 和 Env 的区别
* arg 是在 build 的时候存在的, 可以在 Dockerfile 中当做变量来使用
* env 是容器构建好之后的环境变量, 不能在 Dockerfile 中当参数使用

### 小技巧
1. 拷贝一个文件夹到容器里的命令是
**COPY src WORKDIR/src**
