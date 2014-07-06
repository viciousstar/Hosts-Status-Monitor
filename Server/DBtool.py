# coding: utf8
'''
对数据库的特殊操作
最后修改：张实唯2014.7.5
'''
import pymongo
import load
import save

db = pymongo.Connection('localhost',27017)['hoststatus']

def index():
	a = lambda x: forall(ensureindex(x))
	return a('time'),a('daytime'),a('hourtime')
def archive():
	pass

#small funcs
def forall(f):
	return [f(col) for col in (db[name] for name in db.collection_names() if name not in ['system.indexes'])]
def ensureindex(colname):
	return lambda col:col.ensure_index(colname,pymongo.DESCENDING)
