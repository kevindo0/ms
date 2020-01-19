FROM ubuntu:16b

COPY install.sh /root

RUN bash /root/install.sh

EXPOSE 5672
EXPOSE 15672

ENTRYPOINT ["/usr/sbin/rabbitmq-server"]