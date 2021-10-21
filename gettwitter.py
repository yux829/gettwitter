import twint
import time
import json
import daos
from models import Tweet
import datetime
import os
import daos


def queryTweet(queryName, since, until, proxy):
    c = twint.Config()
    if proxy:
        c.Proxy_host = proxy.split(':')[0]
        c.Proxy_port = proxy.split(':')[1]
        c.Proxy_type = 'HTTP'
    c.Search = "(from:"+queryName+")"
    if since:
        c.Since = since + ' 00:00:00'
    if until:
        c.Until = until + ' 00:00:00'
    fileName = str(time.strftime("%Y%m%d%H%M%S", time.localtime())) + ".json"
    c.Output = fileName
    c.Store_json = True
    print(queryName+'-'+since+'-'+until+'-')
    twint.run.Search(c)
    #print('ok...')
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
    #print(queryName + '-'+since+'-'+until+'-'+' is not data !')


def getAndSave(queryName, since, until, proxy):
    fileName = query4Tweet(queryName, since, until, proxy)
    if fileName:
        datas = getJsonData(queryName, fileName)
        for data in datas:
            #print(data)
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

def getAndSaveAndShow(queryName, since, until,queryTypeIsView,queryTypeIsAll, proxy):
    if queryTypeIsView:
        return queryByQueryName2(queryName, None, None)
    elif queryTypeIsAll:
        #循环处理

        return queryByQueryName2(queryName, None, None)
    else :
        getAndSave(queryName, since,until,proxy)
        return queryByQueryName2(queryName, since, until)
   


if __name__ == '__main__':
    datas = getAndSaveAndShow(
        'realsatoshinet', '2021-01-03', '2021-01-20', '127.0.0.1:11000')
    #for data in datas:
        #print(data)
    print('finished.......')
