FROM ubuntu:16b

RUN apt-get update && apt-get install -y curl apt-transport-https bzip2

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs build-essential

# 淘宝镜像cnpm安装
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt-get update && apt-get install -y yarn