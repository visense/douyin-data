#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import requests

# conn = sqlite3.connect('userData.sqlite')
# print "Opened database successfully"
# c = conn.cursor()
# c.execute('''CREATE TABLE COMPANY
#       (
#         ID            INT         NOT NULL,
#         DOUYIN_ID     CHAR(20),
#         NAME          CHAR(20),
#         SIGNA         CHAR(120),
#         LOCATION      CHAR(10),
#         CONSTELLATION CHAR(5),
#         FOCUS         INT,
#         FOLLOWER      INT,
#         Liked         INT,
#         VIDEO         INT,
#         like          INT
#       );''')
# print "Table created successfully"
# conn.commit()
# conn.close()

# 截取字符串
def subString(str, start, end, startInd = 0):
  startIndex = str.find(start.decode('utf-8'), startInd)
  if (startIndex == -1): return ''
  # print(startIndex)
  endIndex = str.find(end.decode('utf-8'), startIndex + 1)
  if (endIndex == -1): return ''
  # print(endIndex)
  # print(str[startIndex + len(start):endIndex])
  return str[startIndex + len(start.decode('utf-8')):endIndex]

# 截取字符串组
def subStringArr(str, start, end):
  arr = []
  nextIndex = 0
  while True:
    nextIndex = str.find(start.decode('utf-8'), nextIndex + 1)
    if nextIndex == -1:
      return arr
    temp = subString(str, start, end, nextIndex)
    if str == '':
      return arr
    arr.append(temp)
    # print start.decode('utf-8')
    
    # print nextIndex
  # endIndex = str.index(end.decode('utf-8'), startIndex + 1)
  # print(endIndex)

def fontDecrypt(arr):
  mapList1 = {
    'xe60c': '4',
    'xe60d': '0',
    'xe60d': '0'
  }
  mapList = {
    'xe60d': '0',
    'xe616': '0',
    'xe610': '0',
    'xe61a': '0',
    'xe611': '0',
    'xe602': '1',
    'xe605': '2',
    'xe617': '2',
    'xe613': '7',
    'xe604': '3',
    'xe60c': '4',
    'xe619': '4',
    'xe606': '4',
    'xe607': '5',
    'xe608': '6',
    'xe61f': '6',
    'xe612': '6',
    'xe603': '7',
    'xe61c': '7',
    'xe60a': '7',
    'xe60b': '8',
    'xe615': '8',
    'xe61e': '8',
    'xe609': '9',
    '.': '.',
    'w': 'w'
  }
  str = ''
  for item in arr:
    print item
    if (mapList[item]):
      str += mapList[item]
    else:
      str += item
  return str
# 没有headers会返回页面不存在
headers = {
  "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
}
res = requests.get('https://www.douyin.com/share/user/58803201952', headers = headers)
res.encoding = 'utf-8'

# print(res.text)
# 名字
print(subString(res.text, 'class="nickname">', '</p>'))
# 抖音ID
print(subString(res.text, '抖音ID：     ', '<i'))
# 签名
# print(subString(res.text, '"signature">', '</p>'))
# 城市
print(subString(res.text, '"location">', '</span>'))
# 星座
print(subString(res.text, '"constellation">', '</span>'))

# 关注
focusHtml = subString(res.text, 'class="focus block">', '<span class="text"')
# 针对小数点做特殊处理
focusHtml = focusHtml.replace('.', '&#.;')
# 针对万做特殊处理
focusHtml = focusHtml.replace('</i>w </span>', '&#w;')
focusFont = subStringArr(focusHtml, '&#', ';')
print(fontDecrypt(focusFont))

# 粉丝
followerHtml = subString(res.text, 'class="follower block">', '<span class="text"')
# 针对小数点做特殊处理
followerHtml = followerHtml.replace('.', '&#.;')
# 针对万做特殊处理
followerHtml = followerHtml.replace('</i>w </span>', '&#w;')
followerFont = subStringArr(followerHtml, '&#', ';')
print(fontDecrypt(followerFont))

# 粉丝
likedHtml = subString(res.text, 'class="liked-num block">', '<span class="text"')
# 针对小数点做特殊处理
likedHtml = likedHtml.replace('.', '&#.;')
# 针对万做特殊处理
likedHtml = likedHtml.replace('</i>w </span>', '&#w;')
likedFont = subStringArr(likedHtml, '&#', ';')
print(fontDecrypt(likedFont))
# subString('sdssdaardsddddddd1515', 'sdaar', '1515')