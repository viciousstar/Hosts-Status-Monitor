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
def getcount(name):
	return db[name].count
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
def getext(name,column,Zfilter = {}):
	a = lambda x:db[name].find(Zfilter).sort(column,x).next()[column]
	return a(1),a(-1)
def count(name):
	return db[name].count()
def popby(name,column,Zfilter = {}):
	cursor = db[name].find(Zfilter).sort(column,pymongo.DESCENDING)
	i = cursor.__iter__()
	b = {}
	b[2] = False
	while True:
		if not b[2]:
			try:
				b[1] = i.next()
				b[0]= b[1][column]
				b[2] = True
			except:
				return
		def a():
			yield b[1]
			while True:
				try:
					b[1] = i.next()
				except:
					b[2] = False
					return
				if b[0] == b[1][column]:
					yield b[1]
				else:
					b[0] = b[1][column]
					return
		yield a()
	
		
