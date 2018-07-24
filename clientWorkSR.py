# send and receive  client work
# "clientReceive" -> {"url":"xxx.onio","level":"1,2,3,4,5"}
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
    def __init__(self,url,level):
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
        infor = {"url": self.url, "level": self.level}
        body = json.dumps(infor)
        channel.basic_publish(exchange='', routing_key=self.queueStartName, body=body)
        connectionRabbitMQ.close()

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
        channel.basic_qos(prefetch_count=1)
        result = {}
        for method_fram, properties, body in channel.consume(self.queueResultName):
            result = json.loads(body)
            print "Receive client result: " + body
            channel.basic_ack(delivery_tag=method_fram.delivery_tag)
            break
        connection.close()
        return result



    
