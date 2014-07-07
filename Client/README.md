Client stastics catch:
=====================

传递数据格式

dict
{
"mer": 内存使用百分比

"cpu": cpu使用百分比

"Id": 被监测设备的hostname

"ior": 总线读流量

"iow": 总线写流量
}


程序配置：直接编辑config.py

local_port: 本地监听端口

server_ip: 服务器ip

server_port: 服务器端口

speed_low: 平时收集数据的间隔（单位：秒）

speed_high: 高峰收集间隔
