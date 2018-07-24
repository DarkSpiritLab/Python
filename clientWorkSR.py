# send and receive  client work
# "clientReceive" -> {"url":"xxx.onio","level":"1,2,3,4,5","num":10}
# "clientEnd" -> {"url":"xxx.onio","state":"end"}
# "clientResult" <-  {"ip":localIP,"url":workList["url"],"level":workList["level"]}
#!/usr/bin/python
# -*- coding: UTF-8 -*

import urllib
import urllib2
import json
import time
import pika
from rabbitMq import rabbitMQ

class clientWork:
    queueStartName = "clientReceive"
    queueEndName = "clientEnd"
    queueResultName = "clientResult"
    url = ""
    level = ""
    rabbitMqServerIP = ""
    rabbitMqServerPort = ""
    username = ""
    password = ""
    num=10
    def __init__(self,url,num=10,level="1"):
        self.num =num
        rmq= rabbitMQ()
        self.rabbitMqServerIP = rmq.getIP()
        self.rabbitMqServerPort = rmq.getPort()
        self.username = rmq.getUser()
        self.password = rmq.getPassword()
        self.url=url
        self.level=level

    # senf work
    def sendStart(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        connectionRabbitMQ = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitMqServerIP, self.rabbitMqServerPort, '/', credentials))
        channel = connectionRabbitMQ.channel()
        channel.queue_declare(queue=self.queueStartName)
        infor = {"url": self.url, "level": self.level, "num":self.num}
        body = json.dumps(infor)
        channel.basic_publish(exchange='', routing_key=self.queueStartName, body=body)
        connectionRabbitMQ.close()

    # un use
    def sendEnd(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        connectionRabbitMQ = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitMqServerIP, self.rabbitMqServerPort, '/', credentials))
        channel = connectionRabbitMQ.channel()
        channel.queue_declare(queue=self.queueEndName)
        infor = {"url": self.url, "level": self.level, "state": False}
        body = json.dumps(infor)
        channel.basic_publish(exchange='', routing_key=self.queueEndName, body=body)
        connectionRabbitMQ.close()

    def receiveClient(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        connectionRabbitMQ = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitMqServerIP, self.rabbitMqServerPort, '/', credentials))
        channel = connectionRabbitMQ.channel()
        channel.queue_declare(queue=self.queueResultName)
        #channel.basic_qos(prefetch_count=1)
        result = []
        for method_fram, properties, body in channel.consume(self.queueResultName):
            infor = json.loads(body)
            channel.basic_ack(delivery_tag=method_fram.delivery_tag)
            if infor["url"] == self.url:
                print "Receive client result: " + body
                result.append(infor["ip"])
                if len(result) == self.num:
                    break
            else:
                print "wrong "
                channel.basic_publish(exchange='', routing_key=self.queueResultName, body=body)
                time.sleep(1)
        #channel.cancle()
        connectionRabbitMQ.close()
        return result



    
