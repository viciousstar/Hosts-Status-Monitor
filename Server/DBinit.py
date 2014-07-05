# coding: utf8
'''
对数据库的初始化操作
最后修改：张实唯2014.7.5
'''
import pymongo

db = pymongo.Connection('localhost',27017)['hoststatus']

def init():
	#history.ensure_index('x',pymongo.DESCENDING)
