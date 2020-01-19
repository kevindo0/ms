FROM ubuntu:16b

RUN apt-get update
RUN apt-get install -y libjemalloc-dev

RUN mkdir /etc/redis
COPY redis-server /usr/local/sbin
COPY redis-cli /usr/local/sbin
COPY redis.conf /etc/redis

EXPOSE 6379

CMD ["--requirepass", "123456"]

ENTRYPOINT ["/usr/local/sbin/redis-server", "/etc/redis/redis.conf"]