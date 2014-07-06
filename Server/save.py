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
	return True
	
#small funcs
def addTimeStamp(x):
	x['time'],x['daytime'],x['hourtime'] = time.time(),gettoday(),getnowhour()
	return True
def addArchiveLabel(x):
	x['archivelabel'] = 'none'
	return True
getnowhour = lambda : int(time.time()) / 3600
gettoday = lambda : getnowhour() / 24
def listify(x):
	if type(x) == type({}):
		return [x]
	elif type(x) == type([]):
		return x
	raise Error('传入数据有问题')
def insert(x):
	map(lambda (name,o) : db[name].insert(o) ,[dealId(o) for o in x])
	return True
	
def dealId(data):
	name = data['Id']
	data.pop('Id')
	return name,data
