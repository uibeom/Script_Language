#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback


key = 'fa2b418e06fcf72d99deac9fb61016daf2996a720fba3c638b552124d2d4fbff'
TOKEN = '1864822633:AAHPiJJyJYnrzAdCrHwv2wCx53I775rMHV4'
MAX_MSG_LENGTH = 300
baseurl = 'http://211.237.50.150:7080/openapi/ffdc9d56e6e1acc99dc0304efc850b9764f5668bdc618eb00ecc3f52dcfe17c2/xml/Grid_20200713000000000605_1/1/1000'
bot = telepot.Bot(TOKEN)
# bot.sendMessage('1766332140', '안심식당입니다.')

def getData(loc_param):
    loc_param = loc_param.decode('utf8')
    value = loc_param
    localValue = urllib.parse.quote_plus(value)

    res_list = []
    url = baseurl+ '?' + '&RELAX_SIDO_NM=' + localValue
    print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    rstNum = soup.find('totalcnt')
    rstNum = int(re.sub('<.*?>', '|', rstNum.text))
    if rstNum > 1000:
        rstNum = 1000
    rstName = soup.findAll('relax_rstrnt_nm')
    rstLocation = soup.findAll('relax_add1')
    rstTel = soup.findAll('relax_rstrnt_tel')

    for i in range(rstNum):
        rstName[i] = re.sub('<.*?>', '|', rstName[i].text)
        rstLocation[i] = re.sub('<.*?>', '|', rstLocation[i].text)
        rstTel[i] = re.sub('<.*?>', '|', rstTel[i].text)
        try:
            row = '음식점 이름 : ' + rstName[i] + '\n' + '위치 : ' + rstLocation[i] + '\n' + '전화번호 : ' + rstTel[i] + '\n===================================='
        except IndexError:
            row = item.replace('|', ',')
        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run( param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, param)
        res_list = getData( param)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
