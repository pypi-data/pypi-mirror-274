# -*- coding: utf-8 -*-
# @time: 2024/2/18 10:17
# @author: Dyz
# @file: conn.py
# @software: PyCharm
from tortoise import fields

from du_tools.base_conn import MyModel, load_db
from du_tools.base_spider import BaseDataSpider

db_conf = {
    "connections": {
        "conn": {
            "engine": f"tortoise.backends.mysql",
            "credentials": {
                'host': 'localhost',
                'port': 3306,
                'user': 'dyz',
                'password': 'metstr',
                'database': 'journaldb',
                'charset': 'utf8mb4'
            }
        }
    },
    "apps": {
        "jour": {"models": ["__main__"], "default_connection": "conn"},
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai',
}


class ZkyBase(MyModel):
    class Meta:
        table = 'zky_all'

    # table_description = table.zky_base_desc

    year = fields.IntField(default=0, description='年份')

    abbr = fields.CharField(max_length=1024, default='', null=True, description='期刊简称')
    ename = fields.CharField(max_length=1024, default='', null=True, description='期刊名')

    issn = fields.CharField(max_length=10, default='', null=True, description='issn')
    zky_big = fields.TextField(default='', description='中科院大类-升级版')
    zky_small = fields.TextField(default='', description='中科院小类-升级版')
    # zky_all = fields.TextField(default='', description='中科院升级版-所有数据')
    data = fields.TextField(default='', description='原数据')
    lv = fields.IntField(default=1, description='1=基础版数据, 2=升级版数据')


@load_db(db_conf, create=False)
async def t1():
    data = await ZkyBase.all().values()
    if data:
        for i in data:
            print(i)
    data = await ZkyBase.copy_old()
    print(data)
    data = await ZkyBase.truncate_model()
    print(data)

b = BaseDataSpider( )

b.save_db(t1, 'data')

print(issubclass(ZkyBase, MyModel))
# if __name__ == '__main__':
#     import asyncio
#
#     asyncio.run(t1())
