ServerDoc
=============

##数据交换格式
前->后
data = {
	ID: (代表数组所属机器的字符串)
	CPU: (介于0-100之间的浮点数)
	IO: (正整数)
	MainMemory: (介于0-100之间的浮点数)
}


##1111数据库访问函数

- allinfo() return  {'设备名称1':{CPU:20(百分数),IO:数据,MainMemory:数据},'设备名称2':{CPU:20(百分数),IO:数据,MainMemory:数据},'设备名称3':{CPU:20(百分数),IO:数据,MainMemory:数据}}
- getallname() return ['设备名称1','设备名称2','设备名称3']

