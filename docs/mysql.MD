### 技巧
1.删除外键约束

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

2. ON DUPLICATE KEY UPDATE  
在insert语句后面带上ON DUPLICATE KEY UPDATE 子句，而要插入的行与表中现有记录的惟一索引或主键中产生重复值，那么就会发生旧行的更新；如果插入的行数据与现有表中记录的唯一索引或者主键
不重复，则执行新纪录插入操作。

```sql
INSERT into daily_hit_counter (day, slot, cnt) values ('2017-11-19', 1, 1) ON DUPLICATE KEY UPDATE cnt = cnt + 1;
```

3. 导出表结构和表数据
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
4. 查询显示中文乱码
```sql
show variables like 'character%';
set character_set_client = utf8;
set character_set_connection = utf8;
set character_set_results = utf8;
set character_set_server = utf8;
```

### 2. Error
1. ERROR 1840 (HY000) at line 24: @@GLOBAL.GTID_PURGED can only be set when @@GLOBAL.GTID_EXECUTED is empty   (库迁移的时候，因为涉及从集群迁移到单实例)
```bash
mysqldump -uroot -p --set-gtid-purged=off -d sso > sso1.sql
```
2. 用mysqldump备份数据库时出现when using LOCK TABLES
```bash
mysqldump uroot -p --skip-lock-tables d sso  > sso2.sql
```