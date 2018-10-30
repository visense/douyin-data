#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import time
import base64
from douyin import *

conn = sqlite3.connect('./data/userDataSimple.sqlite')
print("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS SIMPLE
      (
        DOUYIN_ID     CHAR(20),
        NAME          CHAR(20),
        SIGNA         CHAR(120),
        BIRTHDAY      CHAR(10),
        GET_TIME      INT(10)
      );''')
print("Table created successfully")
conn.commit()
conn.close()

UnknownUserList = ['92288104102', '51708353677', '93106195590', '78037370357', '58961747855', '70597792642', '94438297581', '104536537298', '51133864091', '72701488313', '64257944110', '96054122767', '71616235166', '69516110299', '92627905028', '92457069032', '67958766392', '95279651125', '66496572399', '86685315522', '69894587742', '62271636493', '57481506844', '68540600141', '83275612755', '73565287491', '78525724173', '103400503128', '76209252146', '105530182460', '105541040181', '86161907525', '84769567015', '84030501064', '67636369808', '66818313480', '61175757592', '52676148885', '68542400897', '95735052733', '74983799864']

dy = DouyinTool()
# 获取用户关注列表
async def getUserFavorite(user):
  saveUserDataNum = 0
  # 时间
  Time = time.time()
  logging.info("start get follow list")
  # 链接数据库
  # 当然要开启事务啊 不然50W数据就有可能出现数据库锁死那还搞什么搞(我电脑性能差)
  conn = sqlite3.connect('./data/userDataSimple.sqlite', isolation_level=None)
  c = conn.cursor()
  async for video in dy.get_follow_list(user):
    # 从数据库中查找结果
    cursor = c.execute(f"select * from SIMPLE where DOUYIN_ID = {video['user_id']}")
    res = cursor.fetchall()
    # 判断结果是否存在
    if (len(res) == 0):
      # print('save user data:')
      # print(video)
      # 去除换行符
      video['nickname'] = video['nickname'].replace('\n', '')
      video['nickname'] = video['nickname'].replace("'", "''")
      video['signature'] = video['signature'].replace('\n', '')
      video['signature'] = video['signature'].replace("'", "''")
      # 插入用户数据
      # print("Opened database successfully")
      c.execute(f"INSERT INTO SIMPLE (DOUYIN_ID, NAME, SIGNA, BIRTHDAY, GET_TIME) \
        VALUES ({video['user_id']}, '{video['nickname']}', '{video['signature']}', '{video['birthday']}', {int(Time)} )");
      # print("Records created successfully")
      saveUserDataNum += 1
      # 用户池上限100防止溢出
      if (len(UnknownUserList) < 100):
        UnknownUserList.append(video['user_id'])
  UnknownUserList.remove(user)
  # print(str(user))
  logging.info(f"user {str(user)} clear! save data number {str(saveUserDataNum)} strip")
  logging.info(f"current user pool:{str(UnknownUserList)}")
  conn.commit()
  conn.close()

save_dir = 'C:/Users/my/Documents/GitHub/douyin-hack/data/video'
concurrency = 20
user = '69528936131'
action = 'favorite'
follow = False
# trio.run(main, user, action, follow, save_dir, concurrency)
while len(UnknownUserList) > 0:
  trio.run(getUserFavorite, UnknownUserList[0])
logging.info('all over!')