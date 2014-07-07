# coding: utf8
'''
数据可视化处理
最后修改：张实唯2014.7.5
'''
import load

defaults = {
	'cpu': (0,100),
	'ior' : (200000000,1000000000),
	'iow': (200000000,1000000000),
	'mem': (10,100)
}

def percentify(name,column,value):
	a,b = getbound(name,column)
	unit = float(b-a) / 90
	x = 5 + (value-a) / unit
	return bound(0,100)(x)

#small funcs
def getbound(name,column):
	return getmin(name,column),getmax(name,column)
def getmax(name,column):
	if load.count(name) < 30 : return defaultmax(column)
	return load.getext(name,column)[1]
def getmin(name,column):
	if load.count(name) < 30 : return defaultmin(column)
	return load.getext(name,column)[0]
def defaultmax(x):
	return defaults[x][1]
def defaultmin(x):
	return defaults[x][0]
def between(a,b):
	return lambda x: (x - a)*(x - b) < 0
def bound(a,b):
	if a > b : a,b = b,a
	def f(x):
		if x < a : x = a
		if x > b : x = b
		return x
	return f

