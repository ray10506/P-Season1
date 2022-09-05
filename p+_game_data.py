# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:25:22 2021

@author: RB505
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
from IPython.display import display_html
from requests_html import HTMLSession
import nest_asyncio
import json
import asyncio
import openpyxl
from openpyxl import Workbook



def check_team(team):
    if team == "臺北富邦勇士Taipei Fubon Braves":
        return 1
    elif team == "福爾摩沙台新夢想家Formosa Taishin Dreamers":
        return 4
    elif team == "新竹街口攻城獅Hsinchu Jko Lioneers":
        return 3
    else:
        return 2

excel_file = Workbook()
sheet = excel_file.active


excel2 = Workbook()
sheet2 = excel2.active

for k in range(61,70):
    
    url="https://pleagueofficial.com/"
    
    page = requests.get(url)
    page = BeautifulSoup(page.text, "html.parser")
    
    
    
    
    #---------------------日期 場管---------------------------------------------------
    title = ["id","time","place"]
    title_d = [k]
    first = page.find("_ngcontent-uxb-c11",class_ = "mat-cell cdk-column-PlayerName mat-column-PlayerName ng-star-inserted").getText()
    print(first)
    quit()
    del first[0]
    print(first)
    out_t = str(first[0])
    title_d.append(first[0] + " "+ first[1])
    t = first[3].split("\n")
    num=0
    for i in t:
        if i != "":
            title_d.append(i)
            num+=1
            if num ==2:
                break
    #print(title_d)
    
    #------------------------客隊-------------------------------------------------------------
    guest_s = []
    
    team = page.find_all("div",class_ = "col-lg-4 col-4 align-self-center px-2")
    guest = team[0]
    #print(guest,type(guest))
    
    img = guest.select("img")
    img = (str(img[0]).replace("<img src=", "")).replace("/>", "")
    #print(img)
    
    guest = guest.getText().split("\n")
   # print(guest)
    for i in guest:
        if i !="" and (not i.isdigit()):
            guest_s.append(i)
    team_id = check_team(guest_s[1])
    guest_s.append(team_id)
    guest_s.append(img)
    del guest_s[0]
    #print(guest_s,"\n\n\n")
    
    
    #-----------------------------主隊------------------------------------------------------
    home_s = []
    home = team[1]
    
    
    img = home.select("img")
    img = (str(img[0]).replace("<img src=", "")).replace("/>", "")
    #print(img)
    
    home = home.getText().split("\n")
    #print(home)
    for i in home:
        if i !="" and (not i.isdigit()):
            home_s.append(i)
    team_id = check_team(home_s[1])
    home_s.append(team_id)
    home_s.append(img)
    del home_s[0]
    #print(home_s)
    
    #------------------------------分數-----------------------------------------------------
    
    
    session = HTMLSession()
    r=session.get(url,verify=False)
    
    
    d = (r.html.find("tbody",first = True).text).split("\n")
    del d[0]
    #print(d)
    
    
    h_t = 0
    g_t = 0
    for i in range(0,len(d),3):
        guest_s.append(d[i])
        home_s.append(d[i+2])
        if d[i] != '-' and d[i+2] != '-':
            h_t += int(d[i+2])
            g_t+=int(d[i])
    
    title = ["比賽id","time","場館","場次","隊名","主隊id","隊徽",'主隊Q1', '主隊Q2', '主隊Q3', '主隊Q4', '主隊OT', '主隊OT', '主隊Final',"隊名","客隊 id","隊徽",'客隊Q1', '客隊Q2', '客隊Q3', '客隊Q4', '客隊OT', '客隊OT', '客隊Final']
    
    home_s.append(h_t)
    guest_s.append(g_t)
    print(home_s)
    print(guest_s)
    
    
    
   
    if k ==13:
        sheet.append(title)
    
    title_d += home_s + guest_s
    print(title_d)
    
    sheet.append(title_d)
    

    



    
    #-----------------------------比賽個人數據-------------------------------------------------

    json = "https://match.pleagueofficial.com/api/boxscore.php?id=" + str(k) + "&away_tab=total&home_tab=total"
    r = requests.get(json, verify=False)
    data = r.json()
    #print(data)
    data = data["data"]              
    print(type(data))
    print(data,len(data),"\n\n\n\n")
    
    home_list = data["home"]
    away_list = data["away"]
    
    
    t = list(home_list[0].keys())
    key=["比賽id","team id","球員id","name_alt"]
    del t[t.index("name_alt")]
    del t[t.index("player_id")]
    for i in t:
        key.append(i)
        
    
    print(key,"\n\n\n")
    home=[]
    away=[]
    
    print(len(home_list),type(home_list))
   
    for i in home_list:
        t = [str(k)]
        
        t.append(home_s[1])
        t.append(i["player_id"]) 
        t.append(i["name_alt"])
        for x in range(4,len(key)):
            j = key[x]
            
            if j != "name_alt" and j != "player_id" :
                    
                if i[j] == '' or i[j] == None:
                    i[j] = "0"
                
                if j=="seconds" and i[j] == "0":
                    i[j] = "DNP"
                    
                if "%" in str(i[j]):
                    i[j] = i[j].replace("%","")
                    
                if j == "starter":
                    if i[j] == "〇":
                        i[j] = 1
                    else:
                        i[j] = 0
                #print(i[j],end = " ")
                t.append(i[j])
        print(t)
        home.append(t)
    print("\n")
    print("\n\n\n\n")
    
    
    print(len(away_list),type(away_list))
    
    for i in away_list:
        t=[str(k)]
        t.append(guest_s[1])
        t.append(i["player_id"]) 
        t.append(i["name_alt"])
        
        for x in range(4,len(key)):
            j = key[x]
            
            if j != "name_alt" and j != "player_id":
                    
                if i[j] == "" or i[j] == None:
                    i[j] = "0"
                
                if j=="seconds" and i[j] == "0":
                    i[j] = "DNP"
                    
                if "%" in str(i[j]):
                    i[j] = i[j].replace("%","")
                    
                if j == "starter":
                    if i[j] == "〇":
                        i[j] = 1
                    else:
                        i[j] = 0
                #print(i[j],end = " ")
                t.append(i[j])
        print(t)
        away.append(t)

    #-----------------------------------輸出----------------------------------------
    
    
    if k==13:
        sheet2.append(key)
    
    for i in home:
        sheet2.append(i)
        
    for i in away:
        sheet2.append(i)
        
out2 = "C:\\Users\\RB505\\Desktop\\hot\\比賽數據\\playoffs_球員數據.xlsx"
excel2.save(out2)

'''

out = "C:\\Users\\RB505\\Desktop\\hot\\比賽數據\\比賽資料.xlsx"
excel_file.save(out)

'''
