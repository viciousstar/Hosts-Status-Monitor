# coding: utf8
'''
对数据库的读取操作
最后修改：张实唯2014.7.5
'''
import pymongo
import time

db = pymongo.Connection('localhost',27017)['hoststatus']

def allinfo():
	return forall(readlastone,{})
def getallname():
	return filter(lambda x: x not in ['system.indexes'],db.collection_names())
	
#small funcs
def forall(Zfunction,data):
	return [Zfunction(args) for args in (addId(i)(data) for i in db.collection_names() if i not in ['system.indexes'])]
def addId(name):
	def l(o):
		o['Id'] = name
		return o
	return l
def endlessrepeater(something):
	while True:
		yield something
def dealId(data):
	name = data['Id']
	data.pop('Id')
	return name,data
def readintime(Zfilter,limits):
	a,b = dealId(Zfilter)
	return db[a].find(b).sort('time',pymongo.DESCENDING).limit(limits)
def readonewithname(Zfileter):
	a,b = dealId(Zfilter)
	return {a:db[a].find(b).sort('time',pymongo.DESCENDING).next()}
def readlastone(Zfilter):
	a = readonewithname(Zfilter)
	return a.values()[0]

