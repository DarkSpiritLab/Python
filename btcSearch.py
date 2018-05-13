#"btcAddr"  ->    addresses.append({"addr":"1C1mCxRukix1KfegAY5zQQJV7samAciZpv","onio":"onio","user":"username"})
#result.append({"monitor":{},"tx":{}})  ->    "btcResult"

import urllib
import urllib2
import json
import time
import pika
import threading
import  pySetting


rabbitMqServerIP = "10.11.49.71"
rabbitMqServerPort = 5672

username ="test"
password = "test"

url_lastblock = "http://blockchain.info/latestblock" 
url_rawblock = "http://blockchain.info/rawblock/"

credentialsSend = pika.PlainCredentials(username,password)
connectionSend = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentialsSend))
channelSend = connectionSend.channel()
channelSend.queue_declare(queue="btcResult")

addresses = list() #btc address  from rabbitmq


def searchLastblockHash():
    req = urllib2.Request(url_lastblock)
    infor = urllib2.urlopen(req).read()
    blockJson = json.loads(infor)
    return blockJson["hash"]

def searchTransactionByHash(blockhash):
    req = urllib2.Request(url_rawblock+blockhash)
    infor = urllib2.urlopen(req).read()
    blockJson = json.loads(infor)
    tx = blockJson["tx"]
    return tx

def sendResultToRabbitMQ(result):
    infor = json.dumps(result)
    channel.basic_publish(exchange='',routing_key='btcAddr',body=infor)
    
def search():
    global addresses
    while True:
        lastHash = searchLastblockHash()
        #print lastHash
        tranLists = searchTransactionByHash(lastHash)
        result = list()
        for i in tranLists:
            if i.has_key("out") == False:
                break;
            outLists = i["out"]
            #print outLists
            for j in outLists:
               if j.has_key("addr") == False:
                   continue
               for k in addresses:
                   if k["addr"] == j["addr"]:
                       item = {"monitor":k,"tx":j}
                       result.append(item)
        #print "\nresult = addrs = "
        #print result
        #print addresses
        if result:
            sendResultToRabbitMQ(result)
        time.sleep(500)

def receive():
    credentials = pika.PlainCredentials(username,password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentials))
    channel = connection.channel()
    channel.queue_declare(queue="btcAddr")
    channel.basic_qos(prefetch_count=1)
    global addresses
    for method_fram,properties,body in channel.consume("btcAddr"):
        item = json.loads(body)
        addresses.append(item)
        channel.basic_ack(delivery_tag = method_fram.delivery_tag)
    requeued_messages = channel.cancle()
    print ('Requeued %i messages' %requeued_messages)
    connection.close()

if __name__ == "__main__":
    t = threading.Thread(target=receive)
    t.start()
    search()
    connectionSend.close()
