
from models import Tweet
from dbconfig import SessionLocal, engine, Base
import datetime

session = SessionLocal()
Base.metadata.create_all(bind=engine)


def save(tw):
    otw = session.query(Tweet).get(tw.id)
    if otw:
        #print('finded..')
        otw.user_id = tw.user_id
        otw.tweet = tw.tweet
        otw.time = tw.time
        otw.file_name = tw.file_name
        otw.query_name = tw.query_name
    else:
        session.add(tw)
    session.commit()
    session.close()


def queryByQueryName(query_name, since, until):
    if since is None:
        since = (datetime.datetime.now() - datetime.timedelta(days=1000))
    if until is None:
        until = datetime.datetime.now()
    return session.query(Tweet.time, Tweet.tweet).filter(Tweet.query_name == query_name).filter(Tweet.time.between(since, until)).order_by(Tweet.time).all()


if __name__ == '__main__':
    """
       tk = Tweet(id='111', time= datetime.datetime.now(), user_id='111', tweet='test01',file_name='002122')
       save(tk)
       print('ok')

    datas = queryByQueryName('realsatoshinet', None, None)
    for data in datas:
        time = data['time'].strftime("%y-%m-%d %H:%M:%S")
        tweet = data['tweet']
        print(time + '--'+tweet)
    """