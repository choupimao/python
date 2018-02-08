# 数据完整性：

- 一个数据库就是一个完整的业务单元，可以包含多张表，数据被存储在表中
- 在表中为了更加准确的存储数据，保证数据的正常有效，可以在创建表的时候，为表添加一些强制性的验证，包括数据字段的类型、约束。

## 字段类型

- 在MySQL中包含的数据类型很多，这里主要列出来常用的几种
- 数字：int,decimal
- 字符串：varchar,text
- 日期：datetime
- 布尔：bit

## 约束

- 主键primary key
- 非空 not null
- 唯一 ：unique
- 默认：default
- 外键: foreign key

# 数据库操作

- 创建数据库

```mysql
create database dbname charset = 'utf8';
```

- 删除数据库

```mysql
drop database dbname;
```

- 切换数据库

```mysql
use dbname;
```

- 查看当前选择的数据库

```mysql
select database();
```

# 表操作

- 查看当前数据库中所以表

```mysql
show databases;
```

- 创建表
- auto_increment 表示自动增长

```mysql
create table tbname(列及类型);
如：
create table students(
id int auto_increment primary key,
sname varchar(10) not null,
);
```

- 修改表

```mysql
alter table tbname add|change|drop 列名 类型;
如：
alter table students add birthday datetime;
```

- 删除表

```mysql
drop table tbname;
```

- 查看表结构

```mysql
desc tbname;
```

- 更改表名称

```mysql
rename table 原表名 to 新表名；
```

- 查看表的创建语句

```mysql
show create table 'tbname';
```

# 数据操作



