FROM ubuntu:16b

RUN mkdir -p /var/log/mongodb
RUN mkdir -p /var/lib/mongo
RUN mkdir -p /var/run/mongodb
RUN mkdir /etc/mongo

COPY mongod /usr/local/sbin
COPY mongo /usr/local/sbin
COPY mongod.conf /etc/mongo

EXPOSE 27017

ENTRYPOINT ["/usr/local/sbin/mongod", "-f", "/etc/mongo/mongod.conf"]
