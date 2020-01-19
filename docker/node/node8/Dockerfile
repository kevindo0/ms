FROM ubuntu:16b

ENV NODE_VERSION 8.11.3

RUN apt-get update && apt-get install -y curl apt-transport-https bzip2

RUN set -ex \
    && wget https://nodejs.org/dist/v8.11.3/node-v$NODE_VERSION-linux-x64.tar.gz \
    && tar zxf node-v$NODE_VERSION-linux-x64.tar.gz -C /usr/local --strip-components=1 --no-same-owner \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs

# 淘宝镜像cnpm安装
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt-get update && apt-get install -y yarn