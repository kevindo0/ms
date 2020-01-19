### Notice
[dockerfile ubuntu](https://github.com/nodejs/docker-node.git)
[node tar download](https://nodejs.org/dist/v8.11.3/)

### Install
```
apt-get install -y bzip2
npm i -g npm
```
### build
```
docker build -t node:10 .
docker run -d -ti --name node10 --restart on-failure -v /data:/data node:10
```
### yarn
yarn设置淘宝镜像
```
yarn config get registry
# -> https://registry.yarnpkg.com
yarn config set registry https://registry.npm.taobao.org
```