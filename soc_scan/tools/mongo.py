# -*- coding:utf-8 -*-

import logging

from pymongo import MongoClient

from soc import settings

logger = logging.getLogger('soc_scan')


# 数据库连接
class MongoConn(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings.MONGO_DB['DB'], settings.MONGO_DB['PORT'])
            self.db = self.conn[settings.MONGO_DB['DBNAME']]
            self.username = settings.MONGO_DB['DBUSERNAME']
            self.password = settings.MONGO_DB['DBPASSWORD']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception as e:
            logger.error('MongoDb连接失败,请检查配置!', e)
