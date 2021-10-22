#-*- coding:utf-8 -*-
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import InputText
import gettwitter
import datetime
import time
sg.theme('lightgrey2')


    

def main():
    since = (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d")
    until = (datetime.datetime.now()).strftime("%Y-%m-%d")
    data=[]
    header_list = ['时间', '内容']
    layout = [[sg.T('推特',size=(5,1),justification='right'),sg.Combo(['用户名', '关键字'],size=(10,1),default_value='用户名' ,key='key_query_model'),sg.T(':',size=(1,1)),sg.InputText (key='key_query_name',default_text="realsatoshinet",size=(25,1)),sg.T('时间段从:',size=(8,1)),sg.InputText (key='key_since',default_text=since,size=(13,1)),sg.T('至:',size=(3,1),justification='right'),sg.InputText (key='key_util',default_text=until,size=(13,1)),sg.Button('查询')],[sg.T('处理方式:',size=(10,1),justification='right'),sg.Radio('新获取', "query_type",key='key_query_type_new', default=True, size=(5,1)), sg.Radio('只看不获取', "query_type",key='key_query_type_view'),sg.Radio('深度采集(耗时长)', "query_type",key='key_query_type_all'),sg.Checkbox('只看中文', default=False,key='key_lang')],[sg.T('代理服务器:',size=(10,1)),sg.InputText(key='key_proxy',size=(70,2),default_text='127.0.0.1:11000')],[sg.InputText(default_text='备注：推特反爬虫技术过于厉害，查询结果可能不全，望包涵!',font=("微软雅黑", 10),justification='left',readonly = True,size=(110,1))],[sg.Multiline(key='key_output',size=(100, 20), font=('微软雅黑 12'))]]

    window = sg.Window('推特助手', layout, font=("微软雅黑", 12),default_element_size=(100,10) )

    while True:
        event, values = window.read()
        if event in (None, '关闭'):   
            break
        if event == '查询':
            queryName = values['key_query_name']
            since = values['key_since']
            until =values['key_util']
            if until:
                until =until
            else :
                until =(datetime.datetime.now()).strftime("%Y-%m-%d")
            until =getNextday(until,1)
            proxy=values['key_proxy']
            key_query_type_new=values['key_query_type_new']
            queryTypeIsView=values['key_query_type_view']
            queryTypeIsAll=values['key_query_type_all']
            query_model=values['key_query_model']
            key_lang =values['key_lang']
            print(queryName+'-'+since+'-'+until+'-'+str(key_query_type_new)+'-'+str(queryTypeIsView)+'-'+str(queryTypeIsAll)+'-'+query_model+'-'+str(key_lang))
            lang =None
            if key_lang :
                lang='zh-cn'

            userName =None
            keyName = None
            if query_model=='用户名' :
                userName=queryName
            else :
                keyName=queryName
            if queryName :
                datas = gettwitter.getAndSaveAndShow(keyName,userName,lang,since,until,queryTypeIsView,queryTypeIsAll,proxy)
                dataBuffer =''
                if datas:
                    # EXECUTE YOUR COMMAND HERE
                    for data in datas:
                        dataBuffer +=data[0] +'\n'
                        dataBuffer +=data[1] +'\n'
                        dataBuffer +='\n'
                    window['key_output'].update(dataBuffer)
                else :
                    sg.popup('没有查询到结果,可能是名称输入错误,或推特做了反扒处理，请稍后再试试! ')    
            else:
               sg.popup('请输入推特用户名称   ',font=("微软雅黑", 10),line_width=40,title='')
  
    window.close()

def getNextday(datastr,n):
    the_date = datetime.datetime.strptime(datastr, '%Y-%m-%d')
    result_date = the_date + datetime.timedelta(days=n)
    d = result_date.strftime('%Y-%m-%d')
    return d


if __name__ == '__main__':
   main()
