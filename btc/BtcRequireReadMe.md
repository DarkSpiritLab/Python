## 环境

	python2.7
	pika
	jinja2
	
## 相关文件

##### 1. btcToMD.py 
		
	环境：python2.7 pika jinja2	
	
	将内容发送到"btcReport" <- {"fileName":name,"addr":addr,"time":thisTime,"hash":hash,"md":mdInfo}队列中。
	内容依次为 文件名（文件名为“钱包地址_交易哈希_时间戳.md“），钱包地址，交易时间（字符串），交易的哈希，md内容
	
##### 2. btcSearch.py 
	
	环境：python2.7 pika
	
	负责钱包监控
	
##### 3. btcInputAddr.py

	环境：python2 || python3   pika
	
	负责添加钱包监控地址
	
	使用方法： python btcInputAddr.py "钱包地址"
	
##### 4. btc.md

	比特币监控报告模板

##### 5. btcSearchCreateReport.py 

	同 btcSearch 批量测试使用的，无用处
	
##### 6. rabbitMq.py

	所有涉及到pika的模块均需使用的，提供ip等内容。

## 辅助功能

##### md 转 html

	pip install grip
	grip  your_filename.md  --export you_filename.html
