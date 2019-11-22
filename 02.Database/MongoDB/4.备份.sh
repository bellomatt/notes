#!/bin/sh

OUT_DIR=/data/db/mongodb_bak/temp # 临时备份目录

TAR_DIR=/data/db/mongodb_bak/bak_list # 备份存放路径

DB_URI="mongodb://admin:belloai@127.0.0.1:57017/?authSource=admin" # 数据库连接字符串

DAYS=7 # DAYS=7代表删除7天前的备份，即只保留最近7天的备份

DATE=`date +%Y_%m_%d` # 获取当前系统时间

TAR_BAK="mongodb_bak_$DATE.tar.gz" # 最终保存的数据库备份文件名


### 下面正式执行 ###

cd $OUT_DIR

rm -rf $OUT_DIR/*

mongodump --uri $DB_URI -o $OUT_DIR # 备份全部数据库

tar -zcvf $TAR_DIR/$TAR_BAK $OUT_DIR # 压缩为 .tar.gz 格式

find $TAR_DIR/ -mtime +$DAYS -delete # 删除7天前的备份文件
