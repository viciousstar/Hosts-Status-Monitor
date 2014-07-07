# coding: utf8
'''
对数据库的特殊操作
最后修改：张实唯2014.7.5
'''
import pymongo
import load
import save
import time
import config

db = pymongo.Connection('localhost',27017)['hoststatus']

def index():
	a = lambda x: forall(ensureindex(x))
	return a('time'),a('daytime'),a('hourtime')
def archive():
	for i in ['hourtime','daytime']: archiveall(i)
#small funcs
def archiveall(x):
	now = {'daytime':getday(time.time()),'hourtime':gethour(time.time())}
	p={}
	temp = {'hourtime':'none','daytime':'hour'}
	temp = temp[x]
	for k in load.getallname():
		for i in load.popby(k,x,{'archivelabel':temp}):
			for j in i:
				for l in config.INFOS:
					p[l] = p.get(l,0) + j[l]
					p[l,0] = p.get((l,0),0) + 1
			for l in config.INFOS:
				p[l] = p[l] / p[l,0]
				p.pop((l,0))
			p[x] = j[x]
			p['time'] = j['time']
			if x == 'hourtime': p['daytime'] = j['daytime']
			ppp = load.readarchiveddata(k,'time')
			if now[x] == p[x] or p['time'] in ppp:
				p.clear()
				continue
			p['archivelabel'] = x[:-4]
			p['Id'] = k
			save.insert([p])
			p.clear()
def forall(f):
	return [f(col) for col in (db[name] for name in db.collection_names() if name not in ['system.indexes'])]
def ensureindex(colname):
	return lambda col:col.ensure_index(colname,pymongo.DESCENDING)
gethour = lambda x : int(x) / 3600
getday = lambda x : gethour(x) / 24
