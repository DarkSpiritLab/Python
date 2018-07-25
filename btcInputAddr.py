import pika
import json
import sys

from rabbitMq import rabbitMQ

rmq= rabbitMQ()

rabbitMqServerIP = rmq.getIP()
rabbitMqServerPort = rmq.getPort()

username =rmq.getUser()
password = rmq.getPassword()

credentialsSend = pika.PlainCredentials(username,password)
connectionSend = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentialsSend))
channelSend = connectionSend.channel()
channelSend.queue_declare(queue="btcAddr")

btcAddr = {"addr":str(sys.argv[1]),"onio":"testOnio.onio","user":"testUserName"}
print(btcAddr)
infor = json.dumps(btcAddr)

channelSend.basic_publish(exchange='', routing_key='btcAddr', body=infor)

connectionSend.close()
