FROM ubuntu:18.04
MAINTAINER youle

ENV TZ "Asia/Shanghai"

ADD sources.list /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y wget net-tools vim tree iputils-ping locales curl apt-utils

RUN export DEBIAN_FRONTEND=noninteractive && apt-get install -y tzdata
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
#  重新配置tzdata软件包，使得时区设置生效
RUN apt-get -y install debconf && dpkg-reconfigure -f noninteractive tzdata
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get -y install python3.8

# RUN apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
# RUN wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
# RUN tar -xf Python-3.8.0.tgz && cd Python-3.8.0 && ./configure --enable-optimizations && make -j 8 && make altinstall

# install pip python3.8
RUN apt install -y python3.8-distutils
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.8 get-pip.py
