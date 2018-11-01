#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import sqlite3
import time
import base64
import pyodbc
from douyin import *

conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE=Douyin;UID=PUGE;PWD=mmit7750')
print("Opened database successfully")
c = conn.cursor()
print("Table created successfully")
conn.commit()
conn.close()
# return

UnknownUserList = ['77969762988', '52319536811', '67144834512', '72009651854', '69333925262', '93607060991', '100580408009', '69756487298', '68004163212', '81492537665', '59929208148', '96922290008', '105214594502', '59082463193', '60651563116', '96401849366', '71326758625', '86780349023', '52853596036', '62723217893', '70590695607', '71213246754', '53344390734', '105541438858', '102936159354', '87326312174', '17249838352', '103979237842', '99133405493', '103350384070', '58700856792', '94070125292', '104958542236', '93360275680', '93692682780', '72775242902', '96500968278', '85005403600', '85837556756', '101637774147', '94986367181', '62838485107', '104454981846', '84636039727', '98416003567', '60682919978', '65880928292', '67245360884', '98784978247', '84659875985', '60695674309', '58488129370', '11003711997', '60320064563', '73483290838', '101407097034', '52967182383', '101787864814', '103954053804', '70931700881', '60628276043', '93015103227', '62031670581', '100722195856', '101788864466', '62228967930', '63875051020', '74998747742', '58664973788', '96649688496', '85448613704', '100089169608', '61670398424', '85030785327', '70729751963', '68497175793', '54945875722', '64795624031', '6130497847', '70583616697', '63905433149', '83231877080', '95194995186', '58860407970', '83729657130', '7486924579', '72630837231', '105122771322', '66469477081', '91868266534', '92769225088', '104395874148', '78688991212', '100655515719', '105300848560', '78935006330', '67384133114', '69433131973']


dy = DouyinTool()
# 获取用户关注列表
async def getUserFavorite(user):
  saveUserDataNum = 0
  # 时间
  Time = time.time()
  logging.info("start get follow list")
  # noSearchList = []
  userList = dy.get_follow_list(user)
  # 链接数据库
  conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE=Douyin;UID=PUGE;PWD=mmit7750')
  print(userList)
  c = conn.cursor()
  async for video in userList:
    # 从数据库中查找结果
    cursor = c.execute(f"select * from SIMPLE with(updlock) where DOUYIN_ID = '{video['user_id']}'")
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
      # noSearchList.append({user_id: video['user_id'], nickname: video['nickname'], signature: video['signature']})
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