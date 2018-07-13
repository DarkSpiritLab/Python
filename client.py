# "clientReceive" -> {"url":"xxx.onio","level":"1,2,3,4,5"}
# "clientEnd" -> {"url":"xxx.onio","state":"end"}
#!/usr/bin/python
# -*- coding: UTF-8 -*

import urllib
import urllib2
import json
import time
import pika
import threading
from rabbitMq import rabbitMQ

queueName = "clientReceive"
queueEnd = "clientEnd"
workList = {"url":"xxx.onio","state":True,"level":"1"}

rmq= rabbitMQ()

def receiveEnd():
    credentials = pika.PlainCredentials(rmq.getUser(), rmq.getPassword())
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rmq.getIP(), rmq.getPort(), '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queueName)
    channel.basic_qos(prefetch_count=1)
    global  workList
    for method_fram, properties, body in channel.consume(queueName):
        result = json.loads(body)
        print "Receive client end: " + body
        #workList.append(result)
        channel.basic_ack(delivery_tag=method_fram.delivery_tag)
        if result["url"]  == workList["url"]:
            workList["state"]=False
            break
        else:
            channel.basic_publish(exchange='', routing_key=queueEnd, body=body)
    requeued_messages = channel.cancle()
    print ('Requeued %i messages' % requeued_messages)
    connection.close()

def runWork(work):
    workList["url"]=work["url"]
    workList["level"]=work["level"]
    workList["state"]=True
    t = threading.Thread(target=receiveEnd)
    t.start()
    url = workList["url"]
    if not url.startswith("http"):
        url = "http://"+url
    req = urllib2.Request(url)
    while workList["state"]:
        urllib2.urlopen(req)

def receiveWork():
    credentials = pika.PlainCredentials(rmq.getUser(), rmq.getPassword())
    connection = pika.BlockingConnection(pika.ConnectionParameters(rmq.getIP(), rmq.getPort(), '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queueName)
    channel.basic_qos(prefetch_count=1)
    for method_fram,properties,body in channel.consume(queueName):
        result = json.loads(body)
        runWork(result)
        print "Receive client work: " + body
        channel.basic_ack(delivery_tag = method_fram.delivery_tag)
    requeued_messages = channel.cancle()
    print ('Requeued %i messages' %requeued_messages)
    connection.close()

if __name__ == "__main__":
    receiveWork()
