### 1. 技巧
#### 1.删除外键约束

```sql
show create table project_approval;
#  查看结果:
CREATE TABLE `project_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `platform_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_project_group_company_id` (`company_id`),
  KEY `ix_project_group_platform_id` (`platform_id`),
  CONSTRAINT `project_group_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`),
  CONSTRAINT `project_group_ibfk_2` FOREIGN KEY (`platform_id`) REFERENCES `project_platform` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8
alter table project_approval drop FOREIGN key project_group_ibfk_1;
```
#### 2. ON DUPLICATE KEY UPDATE  
在insert语句后面带上ON DUPLICATE KEY UPDATE 子句，而要插入的行与表中现有记录的惟一索引或主键中产生重复值，那么就会发生旧行的更新；如果插入的行数据与现有表中记录的唯一索引或者主键不重复，则执行新纪录插入操作。

```sql
INSERT into daily_hit_counter (day, slot, cnt) values ('2017-11-19', 1, 1) ON DUPLICATE KEY UPDATE cnt = cnt + 1;
```
#### 3. 导出表结构和表数据
```sql
mysqldump -u用戶名 -p密码 -d 数据库名 表名 > 脚本名; 
-- 导出整个数据库结构和数据
mysqldump -h localhost -uroot -p123456 database > dump.sql

-- 导出单个数据表结构和数据
mysqldump -h localhost -uroot -p123456  database table > dump.sql

-- 导出整个数据库结构（不包含数据）
mysqldump -h localhost -uroot -p123456  -d database > dump.sql

-- 导出单个数据表结构（不包含数据）
mysqldump -h localhost -uroot -p123456  -d database table > dump.sql
```
#### 4. 查询显示中文乱码
```sql
show variables like 'character%';
set character_set_client = utf8;
set character_set_connection = utf8;
set character_set_results = utf8;
set character_set_server = utf8;
```
#### 5. 索引
```sql
-- ALTER TABLE用来创建普通索引、UNIQUE索引或PRIMARY KEY索引。
-- column_list指出对哪些列进行索引，多列时各列之间用逗号分隔
ALTER TABLE table_name ADD INDEX index_name (column_list)
ALTER TABLE table_name ADD UNIQUE (column_list)
ALTER TABLE table_name ADD PRIMARY KEY (column_list)
-- CREATE INDEX可对表增加普通索引或UNIQUE索引。
CREATE INDEX index_name ON table_name (column_list)
CREATE UNIQUE INDEX index_name ON table_name (column_list)
-- 可利用ALTER TABLE或DROP INDEX语句来删除索引
DROP INDEX index_name ON talbe_name
ALTER TABLE table_name DROP INDEX index_name
ALTER TABLE table_name DROP PRIMARY KEY
-- 查看索引
show index from tblname;
show keys from tblname;
```
#### 常用sql
```sql
-- 添加列
alter table table_name add column column_name varchar(30);
-- 删除列
alter table table_name drop column column_name;
-- 修改联合主键索引
alter table table_name drop primary key, add primary key (c1, c2);
-- 查看mysql的超时时间方法
show global variables LIKE '%timeout%';
set global wait_timeout=15000;
-- 开启文件记录
set global general_log=on;
set global general_log_file='/tmp/mylog.log';
```

### 2. 知识点
#### 1. distinct
一般是用来去除查询结果中的重复记录的
```sql
select distinct expression[,expression...] from tables [where conditions];
-- 只对一列操作
select distinct name from user;
-- 对多列操作
select distinct name, age from user;
```
```python
sess.query(User.name).all()
# [('lz',), ('lz',), ('lz',)]
sess.query(User.name).distinct().all()
# [('lz',)]
sess.query(User.name, user.status).all()
# [('lz', 1), ('lz', 1), ('lz', 2)]
sess.query(User.name, user.status).distinct().all()
# [('lz', 1), ('lz', 2)]
```

### 3. Error
#### 1. ERROR 1840 (HY000) at line 24: @@GLOBAL.GTID_PURGED can only be set when @@GLOBAL.GTID_EXECUTED is empty   (库迁移的时候，因为涉及从集群迁移到单实例)
```bash
mysqldump -uroot -p --set-gtid-purged=off -d sso > sso1.sql
```
#### 2. 用mysqldump备份数据库时出现when using LOCK TABLES
```bash
mysqldump uroot -p --skip-lock-tables d sso  > sso2.sql
```
#### 3. 插入表情出错
Incorrect string value: '\\xF0\\x9F\\x90\\xB2'
```sql
-- 查看表中字段字符集
show full columns from user;
-- 编码方式修改成utf8mb4
alter table user modify column name varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci;
```
#### 4. 报错cannot add foreign key constraint
创建外键错误的原因大概有一下几个原因：

1. 关联的两个字段的字段的类型不一致
2. 设置外键删除时set null
3. 两张表的引擎不一致
