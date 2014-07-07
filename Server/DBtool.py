# coding: utf8
'''
对数据库的特殊操作
最后修改：张实唯2014.7.5
'''
import pymongo
import load
import save
import time

db = pymongo.Connection('localhost',27017)['hoststatus']

def index():
	a = lambda x: forall(ensureindex(x))
	return a('time'),a('daytime'),a('hourtime')
def archive():
	today,nowhour = getday(time.time()),gethour(time.time())
	p = {}
	for k in load.getallname():
		for i in load.popby(k,'hourtime',{'archivelabel':'none'}):
			for j in i:
				for l in ['CPU','IO_write','IO_read','MainMemory']:
					p[l] = p.get(l,0) + i[l]
					p[l,0] = p.get((l,0),0) + 1
			for l in ['CPU','IO_write','IO_read','MainMemory']:
				p[l] = p[l] / p[l,0]
				p.pop((l,0))
			p['hourtime'] = j['hourtime']
			p['archivelabel'] = 'hour'
			p['Id'] = k
			save.insert(p)
			p.clear()
				

#small funcs
def forall(f):
	return [f(col) for col in (db[name] for name in db.collection_names() if name not in ['system.indexes'])]
def ensureindex(colname):
	return lambda col:col.ensure_index(colname,pymongo.DESCENDING)
gethour = lambda x : int(x) / 3600
getday = lambda x : gethour(x) / 24
