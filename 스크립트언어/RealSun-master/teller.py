#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import noti

def replyAptData(user, loc_param):
    # loc_param = loc_param.decode('utf8')
    print(user, loc_param)
    res_list = noti.getData( loc_param)
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0])
        print(r)
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'

    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '해당하는 데이터가 없습니다.' )

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text'].encode('utf8')
    inputArgs = text.decode('utf8')
    args = [i for i in inputArgs.split(' ')]
    argsList = ['서울특별시', '인천광역시', '세종특별자치시', '대전광역시', '광주광역시', '대구광역시', '울산광역시', '부산광역시',
                       '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도',
                       '경상북도', '경상남도', '제주특별자치도']

    if args[0] in argsList:
        print('try to ' + args[1])
        replyAptData(chat_id, args[1].encode('utf8'))
    elif args[0] == '그만':
        noti.sendMessage(chat_id, '종료합니다.')

    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n시/도 시/군/구 를 입력하세요.\n(ex) 경기도 시흥시')


