import twint
import time
import json
import daos
from models import Tweet
import datetime
import os
import daos
import pdfkit


def searchStr(queryName, userName, lang):
    queryStr = ''
    if queryName:
        queryStr += queryName + ' '
    if userName:
        queryStr += "(from:"+userName+") "
    if lang:
        queryStr += "lang:"+lang
    print(queryStr)
    return queryStr


def queryTweet(queryName, since, until, proxy):
    c = twint.Config()
    if proxy:
        c.Proxy_host = proxy.split(':')[0]
        c.Proxy_port = proxy.split(':')[1]
        c.Proxy_type = 'HTTP'
    c.Search = queryName
    if since:
        c.Since = since + ' 00:00:00'
    if until:
        c.Until = until + ' 00:00:00'
    fileName = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + ".json"
    c.Output = fileName
    c.Store_json = True
    print(queryName+'-'+since+'-'+until+'-')
    twint.run.Search(c)
    # print('ok...')
    return fileName


def getJsonData(queryName, fileName):
    with open(fileName, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            tweetj = json.loads(line)
            tweet = {}
            tweet['id'] = tweetj['id']
            tweet['user_id'] = tweetj['user_id']
            tweet['time'] = tweetj['date']+" "+tweetj['time']
            tweet['tweet'] = tweetj['tweet']
            tweet['file_name'] = fileName
            tweet['query_name'] = queryName
            yield tweet


def query4Tweet(queryName, since, until, proxy):
    for count in range(4):
        #print('the '+str(count+1)+' call...')
        fileName = queryTweet(queryName, since, until, proxy)
        if os.path.exists(fileName):
            return fileName
    print(queryName + '-'+since+'-'+until+' '+' is not data !')


def getAndSave(queryName, since, until, proxy):
    fileName = query4Tweet(queryName, since, until, proxy)
    if fileName:
        datas = getJsonData(queryName, fileName)
        for data in datas:
            # print(data)
            tw = Tweet(id=data['id'], query_name=data['query_name'], time=datetime.datetime.strptime(
                data['time'], "%Y-%m-%d %H:%M:%S"), user_id=data['user_id'], tweet=data['tweet'], file_name=data['file_name'])
            daos.save(tw)
        os.remove(fileName)


def queryByQueryName2(queryName, since, until):
    datas = daos.queryByQueryName(queryName, since, until)
    results = []
    for data in datas:
        result = []
        result.append(data['time'].strftime("%Y-%m-%d %H:%M:%S"))
        result.append(data['tweet'])
        results.append(result)
    return results


def getAndSaveAndShow(keyName, userName, lang, since, until, queryTypeIsView, queryTypeIsAll, proxy):
    queryName = searchStr(keyName, userName, lang)
    if queryTypeIsView:
        return queryByQueryName2(queryName, None, None)
    elif queryTypeIsAll:
        # 循环查询该用户100天的记录，写到pdf文件中
        today = (datetime.datetime.now()).strftime("%Y-%m-%d")
        deadline = getNextday(today, -365)
        get365days(queryName, proxy, today, deadline)
        datas = queryByQueryName2(queryName, None, None)
        dataBuffer = ''
        if datas:
            for data in datas:
                dataBuffer += data[0] + '\n'
                dataBuffer += data[1] + '\n'
                dataBuffer += '\n'
        fileName=queryName.replace('(','').replace(')', '').replace(' ', '').replace('from:','')+'365.pdf'
        print(fileName)
        savePfd(dataBuffer, fileName)
        return datas
    else:
        getAndSave(queryName, since, until, proxy)
        return queryByQueryName2(queryName, since, until)


def savePfd(content, filename):
    # 将wkhtmltopdf.exe程序绝对路径传入config对象
    path_wkthmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit_options = {'encoding': 'UTF-8'}
    # 生成pdf文件，to_file为文件路径
    cs = content.split('\n')
    contents = ''
    for c in cs:
        contents += c+'<br/>'
    string = ('<html><head><meta charset="UTF-8"></head><body>' +
              contents+'</body></html>')
    pdfkit.from_string(string, filename, configuration=config,
                       options=pdfkit_options)


def get365days(queryName, proxy, today, deadline: datetime):
    nDay = getNextday(today, -5)
    if(nDay >= deadline):
        print('nday:'+nDay+'--deadline:'+deadline+',continue..')
        getAndSave(queryName, nDay, today, proxy)
        get365days(queryName, proxy, nDay, deadline)


def getNextday(datastr, n):
    the_date = datetime.datetime.strptime(datastr, '%Y-%m-%d')
    result_date = the_date + datetime.timedelta(days=n)
    d = result_date.strftime('%Y-%m-%d')
    return d


if __name__ == '__main__':
    since = (datetime.datetime.now()).strftime("%Y-%m-%d")
    since='2021-11-29'
    until =since
    until =getNextday(until,1)
    userName ='LadyofCrypto1'
    #datas = getAndSaveAndShow(
    #    'dydx', 'yux0829', 'zh-cn', '2021-01-19', '2021-10-22', False, False, '127.0.0.1:11000')
    datas = getAndSaveAndShow(None,userName , None,since, until, False, False, '127.0.0.1:11000')
    dataBuffer = ''
    if datas:
            for data in datas:
                #if(data[1].startswith('@')) :
                #    continue
                dataBuffer += data[1] + '\n'
                dataBuffer +='\n'
    fileName=userName.replace('(','').replace(')', '').replace(' ', '').replace('from:','')+'-'+since+'.pdf'
    savePfd(dataBuffer, fileName)
    print('finished.......')
