# coding: utf8
'''
对数据库的初始化操作
最后修改：张实唯2014.7.5
'''
import pymongo

con = pymongo.Connection('localhost',27017)
db = con['hoststatus']
history = db['history']

def init():
	#history.ensure_index('x',pymongo.DESCENDING)
