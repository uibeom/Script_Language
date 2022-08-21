from tkinter import *
import tkinter.ttk
from tkinter import font
from random import *
import spam

# 5/23 추가
import urllib.request

from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus, unquote
import xml.etree.ElementTree as etree
from string import digits

import urllib
import urllib.request
import http.client
import time

import threading
import sys
from tkinter import messagebox
import folium
from cefpython3 import cefpython as cef
import webbrowser
from geopy.geocoders import Nominatim


import requests, xmltodict, json

from PIL import Image, ImageTk

import smtplib

from email.mime.text import MIMEText
import telepot
from pprint import pprint
import teller
import noti


printCount = []
printCountstr =[]

f = open('recommandList.txt', 'rt')
printCount= f.read().split()

print(printCount)
printCount = list(map(int, printCount))

addressBox = []
address = ''
addressIndex = 0
realAddress = ''
class GUI:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("안심식당")
        self.window.geometry("640x570+300+50")  # 너비 x 높이  + 시작x + 시작y
        self.window.configure(bg='light green')
        self.title()
        self.entry()
        self.searchValues()
        self.searchDetailValues(['시/군/구'])
        self.searchCategoryValues()
        self.resultText()
        self.button()
        self.listName()
        self.searchList()
        self.window.mainloop()


    def title(self):
        img = Image.open('image\icon.jpg')
        img = img.resize((100, 100), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(img)
        Label(self.window, image=self.icon).place(x=20, y=20)
        Label(self.window, text="안심식당", width=8, height=1, font=("맑은 고딕", 20, "italic", "bold"),
              bg='light green').place(x=130, y=25)

    def entry(self):
        self.entry = tkinter.Entry(self.window, width=26, borderwidth=10, font=("TkDefaultFont", 14), bg='mint cream')
        self.entry.insert(0, "음식점 이름을 입력하세요")
        self.entry.place(x=140, y=80)
        self.entry.bind("<Button-1>", lambda e: self.entry.delete(0, END))

    def button(self):
        # 버튼
        # 검색버튼
        self.button = tkinter.Button(self.window, text='검색', command=self.search, width=10, height=1, borderwidth=5,
                                     bg='light yellow')
        self.button.place(x=440, y=85)
        # 초기화 버튼
        img5 = Image.open('image\\refreshing.png')
        img5 = img5.resize((20, 20), Image.ANTIALIAS)
        self.refreshIcon = ImageTk.PhotoImage(img5)
        self.button2 = tkinter.Button(self.window, text='초기화', command=self.reset, width=30, height=20, borderwidth=5,
                                      image=self.refreshIcon, bg='light yellow')
        self.button2.place(x=540, y=85)
        # 추천메뉴 버튼
        self.button3 = tkinter.Button(self.window, text='추천메뉴', command=self.recommand, width=10, height=1,
                                      borderwidth=5, bg='light yellow')
        self.button3.place(x=108, y=190)
        # 메일 버튼
        img1 = Image.open('image\gmail.png')
        img1 = img1.resize((30, 30), Image.ANTIALIAS)
        self.gmailIcon = ImageTk.PhotoImage(img1)
        self.button4 = tkinter.Button(self.window, text='메일', command=self.mail, width=30, height=30, borderwidth=3,
                                      image=self.gmailIcon, bg='light yellow')
        self.button4.place(x=370, y=190)
        # 지도 버튼
        img2 = Image.open('image\map.png')
        img2 = img2.resize((30, 30), Image.ANTIALIAS)
        self.mapIcon = ImageTk.PhotoImage(img2)
        self.button5 = tkinter.Button(self.window, text='지도', command=self.map, width=30, height=30, borderwidth=3,
                                      image=self.mapIcon, bg='light yellow')
        self.button5.place(x=465, y=190)
        # 텔레그램 버튼
        img3 = Image.open('image\\telegram.png')
        img3 = img3.resize((30, 30), Image.ANTIALIAS)
        self.telegramIcon = ImageTk.PhotoImage(img3)
        self.button5 = tkinter.Button(self.window, text='텔레그램', command= self.telegram, width=30, height=30, borderwidth=3,
                                      image=self.telegramIcon, bg='light yellow')
        self.button5.place(x=560, y=190)
        # 결과리스트 출력버튼
        img4 = Image.open('image\\rightarrow.png')
        img4 = img4.resize((23, 23), Image.ANTIALIAS)
        self.rightIcon = ImageTk.PhotoImage(img4)
        self.button6 = tkinter.Button(self.window, text='->', command=self.listPrint, width=20, height=20,
                                      borderwidth=3, image=self.rightIcon, bg='light yellow')
        self.button6.place(x=300, y=380)

        #그래프 버튼
        self.graphButton = tkinter.Button(self.window, text='그래프', command=self.graph, width=10, height=1, borderwidth=5,
                                     bg='light yellow')
        self.graphButton.place(x=440, y=45)

    def listName(self):
        self.label = tkinter.Label(self.window, text="목록", width=10, height=1, font=("Arial", 14, "bold"),
                                   bg='light green')
        self.label.place(x=85, y=230)
        self.label2 = tkinter.Label(self.window, text="검색결과", width=10, height=1, font=("Arial", 14, "bold"),
                                    bg='light green')
        self.label2.place(x=420, y=230)

    def searchList(self):
        # 목록1 -> 검색결과 리스트 박스
        self.frame = tkinter.Frame(self.window)

        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tkinter.Listbox(self.frame, selectmode='extended', width=35, height=17,
                                       yscrollcommand=self.scrollbar.set, bg='mint cream')
        self.listbox.pack(side="left")
        self.scrollbar["command"] = self.listbox.yview
        self.frame.place(x=20, y=255)

    def resultText(self):
        self.frame2 = tkinter.Frame(self.window)

        self.scrollbar2 = tkinter.Scrollbar(self.frame2)
        self.scrollbar2.pack(side="right", fill="y")
        self.text = tkinter.Text(self.frame2, width=35, height=21, yscrollcommand=self.scrollbar2.set, bg='mint cream')

        self.text.insert(tkinter.CURRENT, "")

        self.text.pack(side="left")
        self.text.tag_add("강조", "1.0", "1.6")
        self.text.tag_config("강조", background="yellow")
        self.text.tag_remove("강조", "1.1", "1.2")
        self.scrollbar2["command"] = self.text.yview
        self.frame2.place(x=350, y=258)

    def selectValues(self, event):
        self.valuesStr = self.combo1.get()
        self.searchDetailValues(self.valuesStr)

    def searchValues(self):  # 콤보박스 -검색필터 3개
        self.valuesStr = StringVar()
        self.valuesStr = "시/도"

        # values : 시/도
        self.values = ['서울특별시', '인천광역시', '세종특별자치시', '대전광역시', '광주광역시', '대구광역시', '울산광역시', '부산광역시',
                       '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도',
                       '경상북도', '경상남도', '제주특별자치도']

        self.TempFont = font.Font(self.window, size=15, weight='bold', family='Consolas')
        self.combo1 = tkinter.ttk.Combobox(self.window, textvariable=self.valuesStr, font=self.TempFont, width=13,
                                           height=50, values=self.values)
        self.combo1.place(x=30, y=140)
        self.combo1.set(self.valuesStr)
        self.combo1.bind('<<ComboboxSelected>>', self.selectValues)

    def searchDetailValues(self, detailValues):
        self.detailValuesStr = StringVar()
        self.detailValuesStr = "시/군/구"

        if detailValues == '서울특별시':
            self.detailValues = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구'
                                                                                                               '마포구',
                                 '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
        elif detailValues == '인천광역시':
            self.detailValues = ['강화군', '계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '옹진군', '중구']
        elif detailValues == '세종특별자치시':
            self.detailValues = ['전체 읍/면/동']
        elif detailValues == '대전광역시':
            self.detailValues = ['대덕구', '동구', '서구', '유성구', '중구']
        elif detailValues == '광주광역시':
            self.detailValues = ['광산구', '남구', '동구', '북구', '서구']
        elif detailValues == '대구광역시':
            self.detailValues = ['남구', '달서구', '달성군', '동구', '북구', '서구', '수성구', '중구']
        elif detailValues == '울산광역시':
            self.detailValues = ['남구', '동구', '북구', '울주군', '중구']
        elif detailValues == '부산광역시':
            self.detailValues = ['강서구', '금정구', '기장군', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구', '서구', '수영구', '연제구',
                                 '영도구', '중구', '해운대구']
        elif detailValues == '경기도':
            self.detailValues = ['고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시',
                                 '시흥시', '안산시', '안성시', '안양시', '양주시', '여주시', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시',
                                 '평택시', '포천시', '하남시', '화성시']
        elif detailValues == '강원도':
            self.detailValues = ['강릉시', '고성군', '동해시', '삼척시', '속초시', '양구군', '양양군', '영월군', '원주시', '인제군', '정선군', '철원군',
                                 '춘천시',
                                 '태백시', '평창군', '홍천군', '화천군', '횡성군']
        elif detailValues == '충청북도':
            self.detailValues = ['괴산군', '단양군', '보은군', '영동군', '옥천군', '음성군', '제천시', '증평군', '진천구', '청주시', '충주시']
        elif detailValues == '충청남도':
            self.detailValues = ['계룡시', '공주시', '금산군', '논산시', '당진시', '보령시', '부여군', '서산시', '서천군', '아산시', '예산군', '천안시',
                                 '청양군',
                                 '태안군', '홍성군']
        elif detailValues == '전라북도':
            self.detailValues = ['고창군', '군산시', '김제시', '남원시', '무주군', '부안군', '순창군', '완주군', '익산시', '임실군', '장수군', '전주시',
                                 '정읍시', '진안군']
        elif detailValues == '전라남도':
            self.detailValues = ['강진군', '고흥군', '곡성군', '광양시', '구례군', '나주시', '담양군', '목포시', '무안군', '보성군', '순천시', '신안군',
                                 '여수시',
                                 '영광군', '영암군', '완도군', '장성군', '장흥군', '진도군', '함평군', '해남군', '화순군']
        elif detailValues == '경상북도':
            self.detailValues = ['경산시', '경주시', '고령군', '구미시', '군위군', '김천시', '문경시', '봉화군', '상주시', '성주군', '안동시', '영덕군',
                                 '영양군',
                                 '영주시', '영천시', '예천군', '울릉군', '울진군', '의성군', '청도군', '청송군', '칠곡군', '포항시']
        elif detailValues == '경상남도':
            self.detailValues = ['거제시', '거창군', '고성군', '김해시', '남해군', '밀양시', '사천시', '산청군', '양산시', '의령군', '진주시', '창녕군',
                                 '창원시',
                                 '통영시', '하동군', '함안군', '함양군', '합천군']
        elif detailValues == '제주특별자치도':
            self.detailValues = ['제주시', '서귀포시']
        else:
            self.detailValues = ['시/도를 선택하세요!']

        self.combo2 = tkinter.ttk.Combobox(self.window, textvariable=self.detailValuesStr, font=self.TempFont, width=13,
                                           height=50, values=self.detailValues)
        self.combo2.place(x=230, y=140)
        self.combo2.set(self.detailValuesStr)

    def searchCategoryValues(self):
        self.categoryValuesStr = StringVar()
        self.categoryValuesStr = "업종상세"
        # categoryValues : 한식/중식/일식/양식/기타  (기타 : 베트남음식, 필리핀음식 등등 확실하게 알기 어려운 것)
        self.categoryValues = ['한식', '중식', '일식', '서양식', '기타외국식', '기타 음식점업']

        self.combo3 = tkinter.ttk.Combobox(self.window, textvariable=self.categoryValuesStr, font=self.TempFont,
                                           width=13, height=50, values=self.categoryValues)
        self.combo3.place(x=430, y=140)
        self.combo3.set(self.categoryValuesStr)

    def search(self):

        addressBox.clear()

        address=''

        self.listbox.delete(0, 1000)
        self.text.delete(1.0, "end")
        url = 'http://211.237.50.150:7080/openapi/ffdc9d56e6e1acc99dc0304efc850b9764f5668bdc618eb00ecc3f52dcfe17c2/xml/Grid_20200713000000000605_1/1/1000'

        self.valuesStr = self.combo1.get()
        self.detailValuesStr = self.combo2.get()
        self.categoryValuesStr = self.combo3.get()

        if (self.valuesStr != '시/도' and self.detailValuesStr == '시/군/구' and self.categoryValuesStr == '업종상세'):
            parme = '?' + '&RELAX_SI_NM=' + self.valuesStr

        elif (self.valuesStr != '시/도' and self.detailValuesStr != '시/군/구' and self.categoryValuesStr == '업종상세'):
            parme = '?' + '&RELAX_SI_NM=' + self.valuesStr + '&RELAX_SIDO_NM=' + self.detailValuesStr

        elif (self.valuesStr != '시/도' and self.detailValuesStr != '시/군/구' and self.categoryValuesStr != '업종상세'):
            parme = '?' + '&RELAX_SI_NM=' + self.valuesStr + '&RELAX_SIDO_NM=' + self.detailValuesStr + '&RELAX_GUBUN_DETAIL=' + self.categoryValuesStr

        elif (self.valuesStr == '시/도' and self.detailValuesStr == '시/군/구' and self.categoryValuesStr == '업종상세'):
            parme = ""

        url = url + parme
        content = requests.get(url).content
        dic = xmltodict.parse(content)
        jsonString = json.dumps(dic, ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        n = 0
        self.box2 = []

        for item in jsonObj['Grid_20200713000000000605_1']['row']:
            # print(self.categoryValuesStr)
            if item['RELAX_RSTRNT_NM'] == self.entry.get() and self.entry.get() != "음식점 이름을 입력하세요":  # 검색어가 있고 같은 이름의 식당이 있을 떄
                if item['RELAX_GUBUN_DETAIL'] == self.categoryValuesStr:
                    self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                    if item['RELAX_RSTRNT_TEL'] == None:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item['RELAX_GUBUN_DETAIL'])
                        addressBox.append(item['RELAX_ADD1'])
                    else:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item[
                            'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                        addressBox.append(item['RELAX_ADD1'])
                    n += 1
                elif self.categoryValuesStr == '업종상세':
                    self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                    if item['RELAX_RSTRNT_TEL'] == None:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item['RELAX_GUBUN_DETAIL'])
                        addressBox.append(item['RELAX_ADD1'])
                    else:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item[
                            'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                        addressBox.append(item['RELAX_ADD1'])
                    n += 1

            elif self.entry.get() == "음식점 이름을 입력하세요" or self.entry.get() == '':  # 검색어가 없을 떄
                if item['RELAX_GUBUN_DETAIL'] == self.categoryValuesStr:
                    self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                    if item['RELAX_RSTRNT_TEL'] == None:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item['RELAX_GUBUN_DETAIL'])
                        addressBox.append(item['RELAX_ADD1'])
                    else:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item[
                            'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                        addressBox.append(item['RELAX_ADD1'])
                    n += 1

                elif self.categoryValuesStr == '업종상세':
                    self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                    if item['RELAX_RSTRNT_TEL'] == None:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item['RELAX_GUBUN_DETAIL'])
                        addressBox.append(item['RELAX_ADD1'])
                    else:
                        self.box2.append("\n\n이름: " +item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " + item[
                            'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                        addressBox.append(item['RELAX_ADD1'])
                    n += 1

    def reset(self):
        # 필터 리셋
        self.valuesStr = '시/도'
        self.combo1.set(self.valuesStr)
        self.detailValuesStr = '시/군/구'
        self.searchDetailValues(self.valuesStr)
        self.combo2.set(self.detailValuesStr)
        self.categoryValuesStr = '업종상세'
        self.combo3.set(self.categoryValuesStr)

        # 검색창 리셋
        self.entry.delete(0, "end")
        self.entry.insert(0, "음식점 이름을 입력하세요")
        # 결과 리셋

        self.listbox.delete(0, 1000)
        self.text.delete(1.0, "end")


    def listPrint(self):
        self.text.delete(1.0, "end")
        self.selection = self.listbox.curselection()
        self.index = self.selection[0]
        int(self.index)
        self.text.insert(1.0, self.box2[self.index])
        addressIndex =  self.index
        address = addressBox[addressIndex]
        realAddress = address
        print(realAddress)

        if "한식" in self.box2[self.index]:
            printCount[0] += 1
        elif "중식" in self.box2[self.index]:
            printCount[1] += 1
        elif "일식" in self.box2[self.index]:
            printCount[2] += 1
        elif "서양식" in self.box2[self.index]:
            printCount[3] += 1
        elif "기타외국식" in self.box2[self.index]:
            printCount[4] += 1
        elif "기타 음식점업" in self.box2[self.index]:
            printCount[5] += 1

        printCountstr = list(map(str, printCount))

        print(printCountstr)
        wr = open('recommandList.txt', 'w+t')
        wr.write(printCountstr[0])
        wr = open('recommandList.txt', 'a+t')
        wr.write(' ' + printCountstr[1])
        wr = open('recommandList.txt', 'a+t')
        wr.write(' ' + printCountstr[2])
        wr = open('recommandList.txt', 'a+t')
        wr.write(' ' + printCountstr[3])
        wr = open('recommandList.txt', 'a+t')
        wr.write(' ' + printCountstr[4])
        wr = open('recommandList.txt', 'a+t')
        wr.write(' ' + printCountstr[5])


    def recommand(self):
        addressBox.clear()

        address = ''

        self.listbox.delete(0, 1000)
        self.text.delete(1.0, "end")
        url = 'http://211.237.50.150:7080/openapi/ffdc9d56e6e1acc99dc0304efc850b9764f5668bdc618eb00ecc3f52dcfe17c2/xml/Grid_20200713000000000605_1/1/1000'

        self.valuesStr = self.combo1.get()
        self.detailValuesStr = self.combo2.get()
        self.categoryValuesStr = self.combo3.get()

        if (self.valuesStr != '시/도' and self.detailValuesStr == '시/군/구' and self.categoryValuesStr == '업종상세'):
            parme = '?' + '&RELAX_SI_NM=' + self.valuesStr

        elif (self.valuesStr != '시/도' and self.detailValuesStr != '시/군/구' and self.categoryValuesStr == '업종상세'):
            parme = '?' + '&RELAX_SI_NM=' + self.valuesStr + '&RELAX_SIDO_NM=' + self.detailValuesStr


        elif (self.valuesStr == '시/도' and self.detailValuesStr == '시/군/구' and self.categoryValuesStr == '업종상세'):
            parme = ""

        url = url + parme
        content = requests.get(url).content
        dic = xmltodict.parse(content)
        jsonString = json.dumps(dic, ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        n = 0
        self.box2 = []
        #RECOMMENTdetail = printCount.index(min(printCount))
        RECOMMENTdetail = spam.FindMaxIndex(printCount[0],printCount[1],printCount[2],printCount[3],printCount[4],printCount[5])
        
        for item in jsonObj['Grid_20200713000000000605_1']['row']:
            if self.entry.get() == "음식점 이름을 입력하세요" or self.entry.get() == '':  # 검색어가 없을 떄
                if self.categoryValuesStr == '업종상세':
                    if RECOMMENTdetail == 0:
                        if item['RELAX_GUBUN_DETAIL'] == "한식":
                            self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                            n += 1
                            if item['RELAX_RSTRNT_TEL'] == None:
                                self.box2.append(
                                "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " +
                                item['RELAX_GUBUN_DETAIL'])
                                addressBox.append(item['RELAX_ADD1'])
                            else:
                                self.box2.append(
                                "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " +
                                item[
                                'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                                addressBox.append(item['RELAX_ADD1'])


                    elif RECOMMENTdetail == 1:
                        if item['RELAX_GUBUN_DETAIL'] == "중식":
                            self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                            n += 1
                            if item['RELAX_RSTRNT_TEL'] == None:
                                self.box2.append(
                                "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " +
                                item['RELAX_GUBUN_DETAIL'])
                                addressBox.append(item['RELAX_ADD1'])
                            else:
                                self.box2.append(
                                "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " +
                                item[
                                'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                                addressBox.append(item['RELAX_ADD1'])

                    elif RECOMMENTdetail == 2:
                        if item['RELAX_GUBUN_DETAIL'] == "일식":
                            self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                            n += 1
                            if item['RELAX_RSTRNT_TEL'] == None:
                                self.box2.append(
                                "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " +
                                item['RELAX_GUBUN_DETAIL'])
                                addressBox.append(item['RELAX_ADD1'])
                            else:
                                self.box2.append(
                                "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item['RELAX_ADD1'] + "\n\n" + "업종: " +
                                item[
                                'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                                addressBox.append(item['RELAX_ADD1'])

                    elif RECOMMENTdetail == 3:
                        if item['RELAX_GUBUN_DETAIL'] == "서양식":
                            self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                            n += 1

                            if item['RELAX_RSTRNT_TEL'] == None:
                                self.box2.append(
                                    "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item[
                                        'RELAX_ADD1'] + "\n\n" + "업종: " +
                                    item['RELAX_GUBUN_DETAIL'])
                                addressBox.append(item['RELAX_ADD1'])
                            else:
                                self.box2.append(
                                    "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item[
                                        'RELAX_ADD1'] + "\n\n" + "업종: " +
                                    item[
                                        'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                                addressBox.append(item['RELAX_ADD1'])

                    elif RECOMMENTdetail == 4:
                        if item['RELAX_GUBUN_DETAIL'] == "기타외국식":
                            self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                            n += 1
                            if item['RELAX_RSTRNT_TEL'] == None:
                                self.box2.append(
                                    "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item[
                                        'RELAX_ADD1'] + "\n\n" + "업종: " +
                                    item['RELAX_GUBUN_DETAIL'])
                                addressBox.append(item['RELAX_ADD1'])
                            else:
                                self.box2.append(
                                    "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item[
                                        'RELAX_ADD1'] + "\n\n" + "업종: " +
                                    item[
                                        'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                                addressBox.append(item['RELAX_ADD1'])

                    elif RECOMMENTdetail == 5:
                        if item['RELAX_GUBUN_DETAIL'] == "기타 음식점업":
                            self.listbox.insert(n, item['RELAX_RSTRNT_NM'])
                            n += 1
                            if item['RELAX_RSTRNT_TEL'] == None:
                                self.box2.append(
                                    "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item[
                                            'RELAX_ADD1'] + "\n\n" + "업종: " +
                                    item['RELAX_GUBUN_DETAIL'])
                                addressBox.append(item['RELAX_ADD1'])
                            else:
                                self.box2.append(
                                    "\n\n이름: " + item['RELAX_RSTRNT_NM'] + "\n\n주소: " + item[
                                            'RELAX_ADD1'] + "\n\n" + "업종: " +
                                    item[
                                        'RELAX_GUBUN_DETAIL'] + "\n\n" + "전화번호: " + item['RELAX_RSTRNT_TEL'])
                                addressBox.append(item['RELAX_ADD1'])


        recommandIndex = randint(0,n)

        recommandName = self.listbox.get(recommandIndex,recommandIndex)
        recommandResult = self.box2[recommandIndex]
        recommandAddress = addressBox[recommandIndex]


        self.listbox.delete(0,n)
        self.listbox.insert(recommandIndex, recommandName)
        self.box2.clear()
        self.box2.append(recommandResult)
        addressBox.clear()
        addressBox.append(recommandAddress)

    def mail(self):#메일 보내기 메뉴 열고 메일 입력에 사용

        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.starttls()
        self.session.login('dmlqja123@gmail.com', 'qetpbvmjuludzkqk')

        self.msg = MIMEText('내용 : ' + self.box2[self.index])
        self.msg['Subject'] = '제목 : 원하는 식당의 정보입니다.'

        self.window3 = tkinter.Tk()
        self.window3.title("이메일 보내기")
        self.window3.geometry("300x300+600+50")  # 너비 x 높이  + 시작x + 시작y
        self.window3.configure(bg='light green')

        self.entry2 = tkinter.Entry(self.window3, width=38, borderwidth=10, font=("TkDefaultFont", 10), bg='mint cream')
        self.entry2.insert(0, "메일을 받을 이메일 주소를 입력하세요")
        self.entry2.place(x=2, y=80)
        self.accept = " "
        self.entry2.bind("<Button-1>", lambda e: self.entry2.delete(0, END))

        self.button7 = tkinter.Button(self.window3, text='보내기', command=self.sendMail, width=10, height=1, borderwidth=5,
                                     bg='white')
        self.button7.place(x=100, y=150)

    def sendMail(self):     #메일 보내기 버튼에 사용
        self.accept = self.entry2.get()
        print(self.accept)
        self.session.sendmail("dmlqja123@gmail.com", self.accept, self.msg.as_string())
        self.session.quit()

    def telegram(self):
        bot = teller.telepot.Bot(noti.TOKEN)
        noti.sendMessage(1766332140, '시/도 시/군/구 를 입력하세요.\n(ex) 경기도 시흥시')
        bot.message_loop(teller.handle)
        pprint(bot.getMe())
        print('Listening...')


    def graph(self):

        self.window2 = tkinter.Tk()
        self.window2.title("그래프")
        self.window2.geometry("640x570+600+50")  # 너비 x 높이  + 시작x + 시작y
        self.window2.configure(bg='light green')

        self.barWidth = ( 640 - 40 ) / 6
        self.Gframe = Frame(self.window2)
        self.Gframe.pack()
        self.canvas = Canvas(self.Gframe, width=640, height=570, bg='light blue')
        self.canvas.pack()
        self.Gtext = "한식: "
        self.color = 'blue'
        for i in range(6):
            if i == 1:
                self.Gtext = "중식: "
                self.color = 'red'
            elif i == 2:
                self.Gtext = "일식: "
                self.color = 'white'
            elif i == 3:
                self.Gtext = "서양식: "
                self.color = 'yellow'
            elif i == 4:
                self.Gtext = "기타외국식: "
                self.color = 'green'
            elif i == 5:
                self.Gtext = "기타 음식점업: "
                self.color = 'black'

            self.canvas.create_rectangle(20 + i * self.barWidth, 570 - 50 - 10 * printCount[i],
                                    20 + (i + 1) * self.barWidth, 570 - 50, fill = self.color)
            self.canvas.create_text(20 + i * self.barWidth + 50, 570 - 40, text= self.Gtext  + str(printCount[i]) )


    def map(self):
        selection = self.listbox.curselection()
        index = selection[0]
        int(index)

        address = addressBox[index]
        print(address)
        app = Nominatim(user_agent='tutorial')
        location = app.geocode(address, language='ko')

        #def showMap(frame):
         #   sys.excepthook = cef.ExceptHook
          #  window_info = cef.WindowInfo(frame.winfo_id())
           # window_info.SetAsChild(frame.winfo_id(), [0, 0, 800, 600])
            #cef.Initialize()
            #browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
            #cef.MessageLoop()


        # 지도 저장
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=16)
        folium.Marker([location.latitude, location.longitude]).add_to(m)
        url = 'map.html'
        m.save(url)
        webbrowser.open(url)

GUI()
