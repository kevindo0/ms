FROM ubuntu:16.04
MAINTAINER youle

ENV TZ "Asia/Shanghai"

ADD sources.list /etc/apt/sources.list
RUN echo "nameserver 202.96.209.5" > /etc/resolv.conf

RUN apt-get update
RUN apt-get install -y wget net-tools vim tree git iputils-ping sshpass tzdata locales curl

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
