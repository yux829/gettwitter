from sqlalchemy import Column,  String, DateTime, Float

from dbconfig import Base
# 模型类，tablename指表名，如果数据库中没有这个表会自动创建，有表则会沿用


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(String(30), primary_key=True, index=True)
    user_id = Column(String(30))
    query_name =Column(String(100))
    time = Column(DateTime)
    tweet = Column(String(1000))
    file_name=Column(String(30))
   

