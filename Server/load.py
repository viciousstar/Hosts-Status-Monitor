# coding: utf8
'''
对数据库的读取操作
最后修改：张实唯2014.7.5
'''
import pymongo
import time

con = pymongo.Connection('localhost',27017)
db = con['hoststatus']
history = db['history']

def load(data):
	data = listify(data)
	map(addTimeStamp,data)
	history.insert(data)
	pass
	
#small funcs
