# "clientReceive" -> {"url":"xxx.onio","level":"1,2,3,4,5"}
# "clientEnd" -> {"url":"xxx.onio","state":False}
#!/usr/bin/python
# -*- coding: UTF-8 -*

import urllib
import urllib2
import json
import time
import pika
import threading
from rabbitMq import rabbitMQ
rmq= rabbitMQ()

queueName = "clientReceive"
queueEnd = "clientEnd"
workList = {"url":"xxx.onio","state":True,"level":"1"}



def receiveEnd():
    print "receiveEnd start"
    credentials = pika.PlainCredentials(rmq.getUser(), rmq.getPassword())
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rmq.getIP(), rmq.getPort(), '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queueEnd)
    channel.basic_qos(prefetch_count=1)
    global  workList
    for method_fram, properties, body in channel.consume(queueEnd):
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
    print "receiveEnd end"

def runWork(work):
    print "runWork start"
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
    print "runWork end"

def receiveWork():
    print "receiveWork start"
    credentials = pika.PlainCredentials(rmq.getUser(), rmq.getPassword())
    connection = pika.BlockingConnection(pika.ConnectionParameters(rmq.getIP(), rmq.getPort(), '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queueName)
    channel.basic_qos(prefetch_count=1)
    for method_fram,properties,body in channel.consume(queueName):
        result = json.loads(body)
        print "Receive client work: " + body
        runWork(result)
        channel.basic_ack(delivery_tag = method_fram.delivery_tag)
    requeued_messages = channel.cancle()
    print ('Requeued %i messages' %requeued_messages)
    connection.close()
    print "receiveWork end"

if __name__ == "__main__":
    receiveWork()
