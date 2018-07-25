# 2018.7.25

	所有涉及到 rabbitmq的pika 均需要同一目录下附带文件  rabbitMq.py 其作用是提供一些基本的 服务器地址等，所以需要调整内容
	
## 客户端访问任务

	python3版本的后缀添加有“_py3”,例如“client_py3.py”
	
### client.py

	环境：pika
	客户端负责发送请求，用于节点追踪
	使用方法： python client.py
	
### clientWorkSR.py

	环境：pika
	负责发布任务
	使用方法：用于python代码中
	from clientWorkSR import clientWork
	c = clientWork("www.baidu.com",5,"1")  #参数为  url，接受任务的客户端数量，等级（这个参数没用）
	c.sendStart()   #  发布任务
	#
	#以下是接受  那些客户端接收了任务
	#是单线程，所以可能会阻塞一段时间
	result=c.receiveClient() #返回内容为一个list  ["10.0.0.1","10.0.0.2","10.0.0.3",…]

# 以下为过去的内容 

# Python

before use :
python 2.7

pip install pika

安装MySQLdb，请访问 http://sourceforge.net/projects/mysql-python ，(Linux平台可以访问：https://pypi.python.org/pypi/MySQL-python)从这里可选择适合您的平台的安装包，分为预编译的二进制文件和源代码安装包。

如果您选择二进制文件发行版本的话，安装过程基本安装提示即可完成。如果从源代码进行安装的话，则需要切换到MySQLdb发行版本的顶级目录，并键入下列命令:

$ gunzip MySQL-python-1.2.2.tar.gz

$ tar -xvf MySQL-python-1.2.2.tar

$ cd MySQL-python-1.2.2

$ python setup.py build

$ python setup.py install

# btcSearch.py

get last block to find list addr

# btcToMD.py

infor to md

#receive.py

socket file  for tor 

#receivehost.py

for host to insert infor into sql from rabbitmq
