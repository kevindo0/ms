### 1. zookerper
1. 下载zookeeper：[下载地址](http://mirrors.hust.edu.cn/apache/zookeeper/) 

 * 在zookeeper-3.4.13目录下，新建文件夹，并命名，例如data。(路径为：/tmp/zookeeper-3.4.13/data)
 * 复制zoo_sample.cfg为zoo.cfg，找到并编辑dataDir=/tmp/zookeeper-3.4.10/data
 * 标志为1的服务器 echo "1" > /data/zookeeper-3.4.13/data/myid
 * zoo.cfg日志文件路径参数dataLogDir, 一般与数据文件存放在不同的盘中
 * 日志文件zookeeper.out
 * server.A=B:C:D中的A是一个数字,表示这个是第几号服务器,B是这个服务器的IP地址，C第一个端口用来集群成员的信息交换,表示这个服务器与集群中的leader服务器交换信息的端口，D是在leader挂掉时专门用来进行选举leader所用的端口。

2. cat zoo.cfg 配置文件内容
```
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/tmp/zookeeper/data
clientPort=2181
server.1=172.17.0.2:20881:30881
server.2=172.17.0.3:20881:30881
server.3=172.17.0.4:20881:30881
```
3. 命令
```bash
wget http://mirrors.hust.edu.cn/apache/zookeeper/zookeeper-3.4.13/zookeeper-3.4.13.tar.gz
zkServer.sh start
zkServer.sh status
zkCli.sh
```
4. [zkdoc](https://godoc.org/github.com/samuel/go-zookeeper/zk)

### 2. kafka
1、 [kafka下载地址](http://kafka.apache.org/downloads) 下载Binary downloads这个类型
2、server.property
  * broker.id 						# 申明当前kafka服务器在集群中的唯一ID
  * delete.topic.enable=true  		# 删除topic设置
  * listeners 						# 申明此kafka服务器需要监听的端口号
  * zookeeper.connect 				# 申明kafka所连接的zookeeper的地址
  * log.retention.hours=48 			# 数据最多保存48小时
  * log.retention.bytes=1073741824 	# 数据最多1G

3、命令参数
  * --replication-factor 1 			# 就是需要创建的副本数量
  * --partitions 3					# 分区数量

4、 命令
```bash
# 启动kafka
./bin/kafka-server-start.sh config/server.properties
# 创建Topic
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test1
# 查看kafka topic列表
./bin/kafka-topics.sh --zookeeper localhost:2181 --list
# 查看kafka特定topic的详情
./bin/kafka-topics.sh --zookeeper localhost:2181 --topic lx_test_topic --describe
# 生产消息
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test1
# 消费消息
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test1 --from-beginning
# 删除消息
./bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic test1
```

### 3. 文章
1. [构建高可用ZooKeeper集群](https://www.jianshu.com/p/a3583eb3b994)
2. [浅谈ZooKeeper集群与Leader选举](https://www.jianshu.com/p/e377d57d10fc)
3. [zookeeper的作用](https://www.jianshu.com/p/c7e8a370117d)