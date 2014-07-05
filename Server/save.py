# coding: utf8
'''
对数据库的存储操作
最后修改：张实唯2014.7.5
'''
import pymongo
import time

db = pymongo.Connection('localhost',27017)['hoststatus']


def save(data):
	data = listify(data)
	map(addTimeStamp,data)
	insert(data)
	pass
	
#small funcs
def addTimeStamp(x):
	x['time'] = time.time()
	return True

def listify(x):
	if type(x) == type({}):
		return [x]
	elif type(x) == type([]):
		return x
	raise Error('传入数据有问题')

def insert(x):
	name = x['Id']
	x.pop('Id')
	db[name].insert(x)
	return True
	
	
