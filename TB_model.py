# -*- coding: utf-8 -*-
# @Date  : 2017-10-06 09:44:17
# @Author: Alan Lau (rlalan@outlook.com)


from peewee import *
from datetime import datetime


sql_db = SqliteDatabase('TBwires.sqlite')
sql_db.connect()


class BaseModel(Model):

    class Meta:
        database = sql_db


class Wires(BaseModel):
    page = IntegerField(null=False)
    url = CharField(null=False)
    title = CharField(null=False)
    price = CharField()
    user_id = CharField()


class Wiresdetails(BaseModel):
    page = IntegerField(null=False)
    url = CharField(null=False)
    title = CharField(null=False)
    price = CharField(null=False)
    user_id = CharField(null=False)
    basicdetail = CharField(null=True)
    comments_num = CharField(null=True)
    comments = CharField(null=True)


if __name__ == '__main__':
    # Wires.create_table()
    Wiresdetails.create_table()
