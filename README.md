# python
豆瓣热点电影，影评，影评人信息以及点评电影
使用的是Mysql数据库
下面是三个数据库的创建代码：

CREATE TABLE `doubanrmdy` (
	`id` INT(6) NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(80) NOT NULL,
	`director` VARCHAR(60) NOT NULL,
	`screenwriter` VARCHAR(60) NOT NULL,
	`actors` VARCHAR(400) NOT NULL,
	`type1` VARCHAR(40) NOT NULL,
	`region` VARCHAR(80) NOT NULL,
	`initialReleaseDate` VARCHAR(120) NULL DEFAULT NULL,
	`runtime` VARCHAR(80) NULL DEFAULT NULL,
	`rating` FLOAT NULL DEFAULT NULL,
	`stars5` VARCHAR(10) NULL DEFAULT NULL,
	`stars4` VARCHAR(10) NULL DEFAULT NULL,
	`stars3` VARCHAR(10) NULL DEFAULT NULL,
	`stars2` VARCHAR(10) NULL DEFAULT NULL,
	`stars1` VARCHAR(10) NULL DEFAULT NULL,
	PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=138
;

CREATE TABLE `doubanyingping` (
	`id` INT(11) NOT NULL DEFAULT '0',
	`title` VARCHAR(50) NOT NULL DEFAULT '0',
	`comment` VARCHAR(255) NULL DEFAULT NULL,
	`comment_user` VARCHAR(255) NULL DEFAULT NULL
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `douban_user` (
	`comment_user` VARCHAR(50) NOT NULL DEFAULT '0',
	`movie` VARCHAR(2000) NOT NULL DEFAULT '0',
	`intro` VARCHAR(3000) NULL DEFAULT NULL,
	`date` VARCHAR(255) NULL DEFAULT NULL,
	`star` VARCHAR(20) NULL DEFAULT NULL
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;

