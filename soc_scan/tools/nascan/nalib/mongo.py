# coding:utf-8
import pymongo
import sys
import os
from soc import settings

sys.path.append(os.path.split(os.path.realpath(__file__))[0] + "/../../")

db_conn = pymongo.MongoClient(settings.MONGO_DB['DB'], settings.MONGO_DB['PORT'])
na_db = getattr(db_conn, settings.MONGO_DB['DBNAME'])
na_db.authenticate(settings.MONGO_DB['DBUSERNAME'], settings.MONGO_DB['DBPASSWORD'])
NA_INFO = na_db.Info
NA_HISTORY = na_db.History
